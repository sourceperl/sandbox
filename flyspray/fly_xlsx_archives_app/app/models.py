from typing import List, Optional

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class FlysprayAdminRequest(Base):
    __tablename__ = "flyspray_admin_requests"

    request_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(default=0)
    task_id: Mapped[int] = mapped_column(default=0)
    submitted_by: Mapped[int] = mapped_column(default=0)
    request_type: Mapped[int] = mapped_column(default=0)
    reason_given: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    time_submitted: Mapped[int] = mapped_column(default=0)
    resolved_by: Mapped[int] = mapped_column(default=0)
    time_resolved: Mapped[int] = mapped_column(default=0)
    deny_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class FlysprayAssigned(Base):
    __tablename__ = "flyspray_assigned"

    assigned_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "user_id", name="flyspray_task_user"),
        Index("flyspray_task_id_assigned", "task_id", "user_id"),
    )


class FlysprayAttachment(Base):
    __tablename__ = "flyspray_attachments"

    attachment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    comment_id: Mapped[int] = mapped_column(default=0)
    orig_name: Mapped[str] = mapped_column(String(255))
    file_name: Mapped[str] = mapped_column(String(30))
    file_type: Mapped[str] = mapped_column(String(255))
    file_size: Mapped[int] = mapped_column(default=0)
    added_by: Mapped[int] = mapped_column(default=0)
    date_added: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        Index("flyspray_task_id_attachments", "task_id", "comment_id"),
    )


class FlysprayCache(Base):
    __tablename__ = "flyspray_cache"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(4))
    content: Mapped[str] = mapped_column(LONGTEXT)
    topic: Mapped[int] = mapped_column()
    last_updated: Mapped[int] = mapped_column(default=0)
    project_id: Mapped[int] = mapped_column(default=0)
    max_items: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint(
            "type",
            "topic",
            "project_id",
            "max_items",
            name="flyspray_cache_type",
        ),
        Index("flyspray_cache_type_topic", "type", "topic"),
    )


class FlysprayComment(Base):
    __tablename__ = "flyspray_comments"

    comment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("flyspray_tasks.task_id"), default=0
    )
    date_added: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(default=0)
    comment_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_edited_time: Mapped[int] = mapped_column(default=0)

    # Relationships
    task: Mapped["FlysprayTask"] = relationship(back_populates="comments")

    __table_args__ = (Index("flyspray_task_id_comments", "task_id"),)


class FlysprayDependency(Base):
    __tablename__ = "flyspray_dependencies"

    depend_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    dep_task_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "dep_task_id", name="flyspray_task_id_deps"),
    )


class FlysprayGroup(Base):
    __tablename__ = "flyspray_groups"

    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(20))
    group_desc: Mapped[str] = mapped_column(String(150))
    project_id: Mapped[int] = mapped_column(default=0)
    is_admin: Mapped[int] = mapped_column(default=0)
    manage_project: Mapped[int] = mapped_column(default=0)
    view_tasks: Mapped[int] = mapped_column(default=0)
    open_new_tasks: Mapped[int] = mapped_column(default=0)
    modify_own_tasks: Mapped[int] = mapped_column(default=0)
    modify_all_tasks: Mapped[int] = mapped_column(default=0)
    view_comments: Mapped[int] = mapped_column(default=0)
    add_comments: Mapped[int] = mapped_column(default=0)
    edit_comments: Mapped[int] = mapped_column(default=0)
    edit_own_comments: Mapped[int] = mapped_column(default=0)
    delete_comments: Mapped[int] = mapped_column(default=0)
    create_attachments: Mapped[int] = mapped_column(default=0)
    delete_attachments: Mapped[int] = mapped_column(default=0)
    view_history: Mapped[int] = mapped_column(default=0)
    close_own_tasks: Mapped[int] = mapped_column(default=0)
    close_other_tasks: Mapped[int] = mapped_column(default=0)
    assign_to_self: Mapped[int] = mapped_column(default=0)
    assign_others_to_self: Mapped[int] = mapped_column(default=0)
    add_to_assignees: Mapped[int] = mapped_column(default=0)
    view_reports: Mapped[int] = mapped_column(default=0)
    add_votes: Mapped[int] = mapped_column(default=0)
    edit_assignments: Mapped[int] = mapped_column(default=0)
    show_as_assignees: Mapped[int] = mapped_column(default=0)
    group_open: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("group_name", "project_id", name="flyspray_group_name"),
        Index("flyspray_belongs_to_project", "project_id"),
    )


class FlysprayHistory(Base):
    __tablename__ = "flyspray_history"

    history_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(default=0)
    event_date: Mapped[int] = mapped_column(default=0)
    event_type: Mapped[int] = mapped_column(default=0)
    field_changed: Mapped[str] = mapped_column(String(50))
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("flyspray_idx_task_id", "task_id"),)


class FlysprayListCategory(Base):
    __tablename__ = "flyspray_list_category"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(default=0)
    category_name: Mapped[str] = mapped_column(String(30))
    show_in_list: Mapped[int] = mapped_column(default=0)
    category_owner: Mapped[int] = mapped_column(default=0)
    lft: Mapped[int] = mapped_column(default=0)
    rgt: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_project_id_cat", "project_id"),)


class FlysprayListOS(Base):
    __tablename__ = "flyspray_list_os"

    os_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(default=0)
    os_name: Mapped[str] = mapped_column(String(40))
    list_position: Mapped[int] = mapped_column(default=0)
    show_in_list: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_project_id_os", "project_id"),)


class FlysprayListResolution(Base):
    __tablename__ = "flyspray_list_resolution"

    resolution_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resolution_name: Mapped[str] = mapped_column(String(30))
    list_position: Mapped[int] = mapped_column(default=0)
    show_in_list: Mapped[int] = mapped_column(default=0)
    project_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_project_id_res", "project_id"),)


class FlysprayListStatus(Base):
    __tablename__ = "flyspray_list_status"

    status_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status_name: Mapped[str] = mapped_column(String(40))
    list_position: Mapped[int] = mapped_column(default=0)
    show_in_list: Mapped[int] = mapped_column(default=0)
    project_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_project_id_status", "project_id"),)


class FlysprayListTaskType(Base):
    __tablename__ = "flyspray_list_tasktype"

    tasktype_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tasktype_name: Mapped[str] = mapped_column(String(40))
    list_position: Mapped[int] = mapped_column(default=0)
    show_in_list: Mapped[int] = mapped_column(default=0)
    project_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_project_id_tt", "project_id"),)


class FlysprayListVersion(Base):
    __tablename__ = "flyspray_list_version"

    version_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(default=0)
    version_name: Mapped[str] = mapped_column(String(40))
    list_position: Mapped[int] = mapped_column(default=0)
    show_in_list: Mapped[int] = mapped_column(default=0)
    version_tense: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        Index("flyspray_project_id_version", "project_id", "version_tense"),
    )


class FlysprayNotificationMessage(Base):
    __tablename__ = "flyspray_notification_messages"

    message_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    message_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    time_created: Mapped[int] = mapped_column(default=0)


class FlysprayNotificationRecipient(Base):
    __tablename__ = "flyspray_notification_recipients"

    recipient_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(default=0)
    notify_method: Mapped[str] = mapped_column(String(1))
    notify_address: Mapped[str] = mapped_column(String(100))


class FlysprayNotification(Base):
    __tablename__ = "flyspray_notifications"

    notify_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "user_id", name="flyspray_task_id_notifs"),
    )


class FlysprayPref(Base):
    __tablename__ = "flyspray_prefs"

    pref_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pref_name: Mapped[str] = mapped_column(String(20))
    pref_value: Mapped[str] = mapped_column(String(250), default="0")


class FlysprayProject(Base):
    __tablename__ = "flyspray_projects"

    project_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_title: Mapped[str] = mapped_column(String(100))
    theme_style: Mapped[str] = mapped_column(String(20), default="0")
    default_cat_owner: Mapped[int] = mapped_column(default=0)
    intro_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_is_active: Mapped[int] = mapped_column(default=0)
    visible_columns: Mapped[str] = mapped_column(String(255))
    others_view: Mapped[int] = mapped_column(default=0)
    anon_open: Mapped[int] = mapped_column(default=0)
    notify_email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notify_jabber: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notify_reply: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notify_types: Mapped[str] = mapped_column(String(100), default="0")
    feed_img_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feed_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notify_subject: Mapped[str] = mapped_column(String(100), default="")
    lang_code: Mapped[str] = mapped_column(String(10))
    comment_closed: Mapped[int] = mapped_column(default=0)
    auto_assign: Mapped[int] = mapped_column(default=0)
    last_updated: Mapped[int] = mapped_column(default=0)
    default_task: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_entry: Mapped[str] = mapped_column(String(8), default="index")


class FlysprayRegistration(Base):
    __tablename__ = "flyspray_registrations"

    reg_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reg_time: Mapped[int] = mapped_column(default=0)
    confirm_code: Mapped[str] = mapped_column(String(20))
    user_name: Mapped[str] = mapped_column(String(32))
    real_name: Mapped[str] = mapped_column(String(100))
    email_address: Mapped[str] = mapped_column(String(100))
    jabber_id: Mapped[str] = mapped_column(String(100))
    notify_type: Mapped[int] = mapped_column(default=0)
    magic_url: Mapped[str] = mapped_column(String(40))
    time_zone: Mapped[int] = mapped_column(default=0)


class FlysprayRelated(Base):
    __tablename__ = "flyspray_related"

    related_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    this_task: Mapped[int] = mapped_column(default=0)
    related_task: Mapped[int] = mapped_column(default=0)
    is_duplicate: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint(
            "this_task",
            "related_task",
            "is_duplicate",
            name="flyspray_this_task",
        ),
    )


class FlysprayReminder(Base):
    __tablename__ = "flyspray_reminders"

    reminder_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(default=0)
    to_user_id: Mapped[int] = mapped_column(default=0)
    from_user_id: Mapped[int] = mapped_column(default=0)
    start_time: Mapped[int] = mapped_column(default=0)
    how_often: Mapped[int] = mapped_column(default=0)
    last_sent: Mapped[int] = mapped_column(default=0)
    reminder_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class FlyspraySearch(Base):
    __tablename__ = "flyspray_searches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(default=0)
    name: Mapped[str] = mapped_column(String(50))
    search_string: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    time: Mapped[int] = mapped_column(default=0)


class FlysprayTask(Base):
    __tablename__ = "flyspray_tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(default=0)
    task_type: Mapped[int] = mapped_column(default=0)
    date_opened: Mapped[int] = mapped_column(default=0)
    opened_by: Mapped[int] = mapped_column(default=0)
    is_closed: Mapped[int] = mapped_column(default=0)
    date_closed: Mapped[int] = mapped_column(default=0)
    closed_by: Mapped[int] = mapped_column(default=0)
    closure_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    item_summary: Mapped[str] = mapped_column(String(100))
    detailed_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    item_status: Mapped[int] = mapped_column(default=0)
    resolution_reason: Mapped[int] = mapped_column(default=1)
    product_category: Mapped[int] = mapped_column(default=0)
    product_version: Mapped[int] = mapped_column(default=0)
    closedby_version: Mapped[int] = mapped_column(default=0)
    operating_system: Mapped[int] = mapped_column(default=0)
    task_severity: Mapped[int] = mapped_column(default=0)
    task_priority: Mapped[int] = mapped_column(default=0)
    last_edited_by: Mapped[int] = mapped_column(default=0)
    last_edited_time: Mapped[int] = mapped_column(default=0)
    percent_complete: Mapped[int] = mapped_column(default=0)
    mark_private: Mapped[int] = mapped_column(default=0)
    due_date: Mapped[int] = mapped_column(default=0)
    anon_email: Mapped[str] = mapped_column(String(100), default="")
    task_token: Mapped[str] = mapped_column(String(32), default="0")

    # Relationships
    comments: Mapped[List["FlysprayComment"]] = relationship(back_populates="task")

    __table_args__ = (
        Index("flyspray_attached_to_project", "project_id"),
        Index("flyspray_task_severity", "task_severity"),
        Index("flyspray_task_type", "task_type"),
        Index("flyspray_product_category", "product_category"),
        Index("flyspray_item_status", "item_status"),
        Index("flyspray_is_closed", "is_closed"),
        Index("flyspray_closedby_version", "closedby_version"),
        Index("flyspray_due_date", "due_date"),
    )


class FlysprayUser(Base):
    __tablename__ = "flyspray_users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(32))
    user_pass: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    real_name: Mapped[str] = mapped_column(String(100))
    jabber_id: Mapped[str] = mapped_column(String(100))
    email_address: Mapped[str] = mapped_column(String(100))
    notify_type: Mapped[int] = mapped_column(default=0)
    notify_own: Mapped[int] = mapped_column(default=0)
    account_enabled: Mapped[int] = mapped_column(default=0)
    dateformat: Mapped[str] = mapped_column(String(30), default="")
    dateformat_extended: Mapped[str] = mapped_column(String(30), default="")
    magic_url: Mapped[str] = mapped_column(String(40), default="")
    tasks_perpage: Mapped[int] = mapped_column(default=0)
    register_date: Mapped[int] = mapped_column(default=0)
    time_zone: Mapped[int] = mapped_column(default=0)
    login_attempts: Mapped[int] = mapped_column(default=0)
    lock_until: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("user_name", name="flyspray_user_name"),
    )


class FlysprayUsersInGroup(Base):
    __tablename__ = "flyspray_users_in_groups"

    record_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(default=0)
    group_id: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="flyspray_group_id_uig"),
        Index("flyspray_user_id_uig", "user_id"),
    )


class FlysprayVote(Base):
    __tablename__ = "flyspray_votes"

    vote_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(default=0)
    task_id: Mapped[int] = mapped_column(default=0)
    date_time: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("flyspray_task_id_votes", "task_id"),)
