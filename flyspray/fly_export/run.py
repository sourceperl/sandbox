#!/usr/bin/env python3

""" 
Export data from flyspray to a CSV file.

"""

import argparse
from codecs import BOM_UTF8
import csv
from datetime import datetime
from os.path import join
import time
# apt install python3-pymysql
import pymysql
# apt install python3-schedule
import schedule
from private_data import DB_USER, DB_PWD


# some const
PUB_PATH = '/var/www/html/pub/'


# some const
SQL = """
SELECT  t.task_id, p.project_title, c.category_name, s.status_name, tt.tasktype_name, 
        t.item_summary, t.detailed_desc,
        t.date_opened, t.date_closed, t.last_edited_time, 
        uo.user_name AS opened_by_user,
        ua.user_name AS assigned_user,
        COUNT(cm.comment_id) AS comments_nb
  FROM  flyspray_tasks AS t
  LEFT JOIN  flyspray_projects AS p ON t.project_id = p.project_id
  LEFT JOIN  flyspray_list_category AS c ON t.product_category = c.category_id
  LEFT JOIN  flyspray_list_status AS s ON t.item_status = s.status_id
  LEFT JOIN  flyspray_list_tasktype AS tt ON t.task_type = tt.tasktype_id
  LEFT JOIN  flyspray_users AS uo ON t.opened_by = uo.user_id
  LEFT JOIN  flyspray_assigned AS a ON t.task_id = a.task_id
  LEFT JOIN  flyspray_users AS ua ON a.user_id = ua.user_id
  LEFT JOIN  flyspray_comments AS cm ON t.task_id = cm.task_id
  WHERE t.date_opened BETWEEN {from_ts} and {to_ts} OR t.last_edited_time BETWEEN {from_ts} and {to_ts}
  GROUP BY t.task_id
  ORDER BY t.task_id DESC LIMIT 5000
"""

CSV_FIELDS = ['task_id', 'project_title', 'category_name', 'status_name', 'tasktype_name', 'opened_by_user', 'last_edited_time', 'date_opened', 'date_closed',
              'assigned_user', 'comments_nb', 'item_summary', 'detailed_desc']


# some class
class ExcelFr(csv.excel):
    delimiter = ';'


csv.register_dialect('excel-fr', ExcelFr())


# schedule job(s)
def export_job(db: str, fly_id: str, exp_year: int = None):
    try:
        # define export params
        exp_year = exp_year if exp_year else datetime.now().year
        exp_file = join(PUB_PATH, fly_id, f'fly_{fly_id}_{exp_year}.csv')
        sql_open_from_ts = round(datetime(exp_year, 1, 1, 0, 0, 0).timestamp())
        sql_open_to_ts = round(datetime(exp_year, 12, 31, 23, 59, 59).timestamp())

        # connect to DB
        db = pymysql.connect(db=db,
                             user=DB_USER,
                             password=DB_PWD,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        with db.cursor() as cursor:
            # do request
            sql_req = SQL.format(from_ts=sql_open_from_ts, to_ts=sql_open_to_ts)
            if cursor.execute(sql_req):
                with open(exp_file, 'w') as out_file:
                    # write an UTF-8 BOM (for overide default charset on Excel)
                    out_file.write(BOM_UTF8.decode('utf8'))
                    # build CSV
                    w = csv.DictWriter(out_file, fieldnames=CSV_FIELDS,
                                       extrasaction='ignore', dialect='excel-fr')
                    # add header line
                    w.writeheader()
                    # add lines
                    for d in cursor.fetchall():
                        # update datetime fields (timestamp -> str date)
                        for (k, v) in d.items():
                            if k.startswith('date_') or k.endswith('_time'):
                                ts = int(v)
                                if ts > 0:
                                    d[k] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                else:
                                    d[k] = ''
                        # add current line to CSV
                        w.writerow(d)
    except Exception as e:
        print(f'error occur during export_job run: {e} ')


if __name__ == '__main__':
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rebuild', action='store_true', help='rebuild mode (from 2010 to now, then exit)')
    args = parser.parse_args()

    # for rebuild purpose
    if args.rebuild:
        for y in range(2010, datetime.now().year):
            export_job(db='flyspray-tca', fly_id='tca', exp_year=y)
            export_job(db='flyspray-tne', fly_id='tne', exp_year=y)
            export_job(db='flyspray-trm', fly_id='trm', exp_year=y)
            export_job(db='flyspray-tvs', fly_id='tvs', exp_year=y)
        exit()

    # init schedule (WARN: server local time is UTC time)
    schedule.every().day.at('23:45').do(lambda: export_job(db='flyspray-tca', fly_id='tca'))
    schedule.every().day.at('23:45').do(lambda: export_job(db='flyspray-tne', fly_id='tne'))
    schedule.every().day.at('23:45').do(lambda: export_job(db='flyspray-trm', fly_id='trm'))
    schedule.every().day.at('23:45').do(lambda: export_job(db='flyspray-tvs', fly_id='tvs'))

    # main loop
    while True:
        schedule.run_pending()
        time.sleep(1)
