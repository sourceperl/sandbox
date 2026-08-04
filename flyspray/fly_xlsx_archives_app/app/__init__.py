"""
Export data from flyspray to xlsx dashboards using SQLAlchemy ORM.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from os.path import join
from pathlib import Path
from typing import List, Optional
from zoneinfo import ZoneInfo

from app.config import DB_HOST, DB_PWD, DB_USER
from app.models import (
    FlysprayAssigned,
    FlysprayComment,
    FlysprayListCategory,
    FlysprayListStatus,
    FlysprayListTaskType,
    FlysprayProject,
    FlysprayTask,
    FlysprayUser,
)
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session


# some dataclass
@dataclass
class TaskInfo:
    fly_id: str
    task_id: int
    project: str
    summary: str
    status: str
    expl_team: str
    evt_nb: int
    open_dt: Optional[datetime] = None
    last_evt_dt: Optional[datetime] = None


def parse_timestamp(ts: Optional[int]) -> Optional[datetime]:
    """
    Convert a Unix UTC timestamp integer to a naive datetime localized to Europe/Paris.

    :param ts: Unix timestamp in seconds (or None/0).
    :return: A naive datetime object in Paris local time, or None if the input is empty.
    """
    if not ts:
        return None
    dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt_utc.astimezone(ZoneInfo("Europe/Paris")).replace(tzinfo=None)


# Core function refactored with SQLAlchemy
def main(pub_path: Path):
    # init list of TaskInfo
    open_task_l: List[TaskInfo] = []

    for db_name, fly_id in [("flyspray-tne", "tne")]:
        # Create MySQL Engine (using pymysql driver under the hood)
        url = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{db_name}?charset=utf8mb4"
        engine = create_engine(url)

        with Session(engine) as session:
            # Construct SQLAlchemy 2.0 statement
            stmt = (
                select(
                    FlysprayTask.task_id,
                    FlysprayProject.project_title,
                    FlysprayListCategory.category_name,
                    FlysprayListStatus.status_name,
                    FlysprayListTaskType.tasktype_name,
                    FlysprayTask.item_summary,
                    FlysprayTask.detailed_desc,
                    FlysprayTask.date_opened,
                    FlysprayTask.date_closed,
                    FlysprayTask.last_edited_time,
                    FlysprayUser.user_name.label("opened_by_user"),
                    func.count(FlysprayComment.comment_id).label("comments_nb"),
                )
                .outerjoin(
                    FlysprayProject,
                    FlysprayTask.project_id == FlysprayProject.project_id,
                )
                .outerjoin(
                    FlysprayListCategory,
                    FlysprayTask.product_category == FlysprayListCategory.category_id,
                )
                .outerjoin(
                    FlysprayListStatus,
                    FlysprayTask.item_status == FlysprayListStatus.status_id,
                )
                .outerjoin(
                    FlysprayListTaskType,
                    FlysprayTask.task_type == FlysprayListTaskType.tasktype_id,
                )
                .outerjoin(
                    FlysprayUser, FlysprayTask.opened_by == FlysprayUser.user_id
                )
                .outerjoin(
                    FlysprayAssigned,
                    FlysprayTask.task_id == FlysprayAssigned.task_id,
                )
                .outerjoin(
                    FlysprayComment,
                    FlysprayTask.task_id == FlysprayComment.task_id,
                )
                # .where(FlysprayTask.is_closed == 0)
                .group_by(FlysprayTask.task_id)
                .order_by(FlysprayTask.task_id.desc())
                .limit(100_000)
            )

            results = session.execute(stmt).all()

            for row in results:
                # Map row fields to TaskInfo struct
                task_info = TaskInfo(
                    fly_id=fly_id,
                    task_id=row.task_id,
                    project=row.project_title,
                    summary=row.item_summary,
                    status=row.status_name,
                    expl_team=row.category_name,
                    evt_nb=row.comments_nb,
                    open_dt=parse_timestamp(row.date_opened),
                    last_evt_dt=parse_timestamp(row.last_edited_time),
                )
                open_task_l.append(task_info)

        # Sort tasks by last event dt descending
        open_task_l = sorted(open_task_l, key=lambda x: x.last_evt_dt or datetime.min, reverse=True)

    # Build XLSX workbook
    if open_task_l:
        wb = Workbook()
        sheet = wb.active

        if sheet is None:
            raise RuntimeError('unable to find default xlsx sheet')

        sheet.title = "Feuil1"

        # Dimensions & Headings
        headers_and_widths = [
            ("Instance", 15.0),
            ("Task ID", 15.0),
            ("Equipe DTS", 20.0),
            ("Date et heure d'ouverture", 30.0),
            ("Date et heure dernier événement", 30.0),
            ("Résumé", 75.0),
            ("Etat du ticket", 25.0),
            ("Equipe d'exploitation", 30.0),
            ("Nb événement", 15.0),
        ]

        for col_idx, (header, width) in enumerate(headers_and_widths, start=1):
            sheet.column_dimensions[get_column_letter(col_idx)].width = width
            sheet.cell(row=1, column=col_idx, value=header)

        # Append rows
        for row_idx, task_info in enumerate(open_task_l, start=2):
            # column "Instance"
            sheet.cell(row=row_idx, column=1, value=task_info.fly_id.upper())
            # column "Task ID"
            sheet.cell(row=row_idx, column=2, value=task_info.task_id)
            # column "Equipe DTS"
            sheet.cell(row=row_idx, column=3, value=task_info.project)
            # column "Date et Heure d'ouverture"
            if task_info.open_dt:
                cell_open = sheet.cell(row=row_idx, column=4, value=task_info.open_dt)
                cell_open.number_format = "dd/mm/yyyy hh:mm"
            # column "Date et Heure dernier événement"
            if task_info.last_evt_dt:
                cell_evt = sheet.cell(row=row_idx, column=5, value=task_info.last_evt_dt)
                cell_evt.number_format = "dd/mm/yyyy hh:mm"
            # column "Résumé"
            sheet.cell(row=row_idx, column=6, value=task_info.summary)
            # column "Etat du ticket"
            sheet.cell(row=row_idx, column=7, value=task_info.status)
            # column "Equipe d'exploitation"
            sheet.cell(row=row_idx, column=8, value=task_info.expl_team)
            # column "Nb événement"
            sheet.cell(row=row_idx, column=9, value=str(task_info.evt_nb))

        # Format styles
        for col in sheet.columns:
            for cell in col:
                cell.alignment = Alignment(horizontal="center")

        tab = Table(
            displayName="Table1",
            ref=f"A1:{get_column_letter(sheet.max_column)}{sheet.max_row}",
        )
        tab.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium14", showRowStripes=True
        )
        sheet.add_table(tab)

        wb.save(filename=join(pub_path, "fly_all_open_tasks.xlsx"))
