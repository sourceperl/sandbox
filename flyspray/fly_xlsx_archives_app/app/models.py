from sqlalchemy import (
    Column,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class FlysprayAdminRequest(Base):
    __tablename__ = "flyspray_admin_requests"

    request_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, default=0)
    task_id = Column(Integer, nullable=False, default=0)
    submitted_by = Column(Integer, nullable=False, default=0)
    request_type = Column(Integer, nullable=False, default=0)
    reason_given = Column(Text, nullable=True)
    time_submitted = Column(Integer, nullable=False, default=0)
    resolved_by = Column(Integer, nullable=False, default=0)
    time_resolved = Column(Integer, nullable=False, default=0)
    deny_reason = Column(String(255), nullable=True)


class FlysprayAssigned(Base):
    __tablename__ = "flyspray_assigned"

    assigned_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "user_id", name="flyspray_task_user"),
        Index("flyspray_task_id_assigned", "task_id", "user_id"),
    )


class FlysprayAttachment(Base):
    __tablename__ = "flyspray_attachments"

    attachment_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    comment_id = Column(Integer, nullable=False, default=0)
    orig_name = Column(String(255), nullable=False)
    file_name = Column(String(30), nullable=False)
    file_type = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False, default=0)
    added_by = Column(Integer, nullable=False, default=0)
    date_added = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("flyspray_task_id_attachments", "task_id", "comment_id"),
    )


class FlysprayCache(Base):
    __tablename__ = "flyspray_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(4), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    topic = Column(Integer, nullable=False)
    last_updated = Column(Integer, nullable=False, default=0)
    project_id = Column(Integer, nullable=False, default=0)
    max_items = Column(Integer, nullable=False, default=0)

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

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    date_added = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False, default=0)
    comment_text = Column(Text, nullable=True)
    last_edited_time = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_task_id_comments", "task_id"),)


class FlysprayDependency(Base):
    __tablename__ = "flyspray_dependencies"

    depend_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    dep_task_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "dep_task_id", name="flyspray_task_id_deps"),
    )


class FlysprayGroup(Base):
    __tablename__ = "flyspray_groups"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(20), nullable=False)
    group_desc = Column(String(150), nullable=False)
    project_id = Column(Integer, nullable=False, default=0)
    is_admin = Column(Integer, nullable=False, default=0)
    manage_project = Column(Integer, nullable=False, default=0)
    view_tasks = Column(Integer, nullable=False, default=0)
    open_new_tasks = Column(Integer, nullable=False, default=0)
    modify_own_tasks = Column(Integer, nullable=False, default=0)
    modify_all_tasks = Column(Integer, nullable=False, default=0)
    view_comments = Column(Integer, nullable=False, default=0)
    add_comments = Column(Integer, nullable=False, default=0)
    edit_comments = Column(Integer, nullable=False, default=0)
    edit_own_comments = Column(Integer, nullable=False, default=0)
    delete_comments = Column(Integer, nullable=False, default=0)
    create_attachments = Column(Integer, nullable=False, default=0)
    delete_attachments = Column(Integer, nullable=False, default=0)
    view_history = Column(Integer, nullable=False, default=0)
    close_own_tasks = Column(Integer, nullable=False, default=0)
    close_other_tasks = Column(Integer, nullable=False, default=0)
    assign_to_self = Column(Integer, nullable=False, default=0)
    assign_others_to_self = Column(Integer, nullable=False, default=0)
    add_to_assignees = Column(Integer, nullable=False, default=0)
    view_reports = Column(Integer, nullable=False, default=0)
    add_votes = Column(Integer, nullable=False, default=0)
    edit_assignments = Column(Integer, nullable=False, default=0)
    show_as_assignees = Column(Integer, nullable=False, default=0)
    group_open = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("group_name", "project_id", name="flyspray_group_name"),
        Index("flyspray_belongs_to_project", "project_id"),
    )


class FlysprayHistory(Base):
    __tablename__ = "flyspray_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False, default=0)
    event_date = Column(Integer, nullable=False, default=0)
    event_type = Column(Integer, nullable=False, default=0)
    field_changed = Column(String(50), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    __table_args__ = (Index("flyspray_idx_task_id", "task_id"),)


class FlysprayListCategory(Base):
    __tablename__ = "flyspray_list_category"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, default=0)
    category_name = Column(String(30), nullable=False)
    show_in_list = Column(Integer, nullable=False, default=0)
    category_owner = Column(Integer, nullable=False, default=0)
    lft = Column(Integer, nullable=False, default=0)
    rgt = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_project_id_cat", "project_id"),)


class FlysprayListOS(Base):
    __tablename__ = "flyspray_list_os"

    os_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, default=0)
    os_name = Column(String(40), nullable=False)
    list_position = Column(Integer, nullable=False, default=0)
    show_in_list = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_project_id_os", "project_id"),)


class FlysprayListResolution(Base):
    __tablename__ = "flyspray_list_resolution"

    resolution_id = Column(Integer, primary_key=True, autoincrement=True)
    resolution_name = Column(String(30), nullable=False)
    list_position = Column(Integer, nullable=False, default=0)
    show_in_list = Column(Integer, nullable=False, default=0)
    project_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_project_id_res", "project_id"),)


class FlysprayListStatus(Base):
    __tablename__ = "flyspray_list_status"

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(40), nullable=False)
    list_position = Column(Integer, nullable=False, default=0)
    show_in_list = Column(Integer, nullable=False, default=0)
    project_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_project_id_status", "project_id"),)


class FlysprayListTaskType(Base):
    __tablename__ = "flyspray_list_tasktype"

    tasktype_id = Column(Integer, primary_key=True, autoincrement=True)
    tasktype_name = Column(String(40), nullable=False)
    list_position = Column(Integer, nullable=False, default=0)
    show_in_list = Column(Integer, nullable=False, default=0)
    project_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_project_id_tt", "project_id"),)


class FlysprayListVersion(Base):
    __tablename__ = "flyspray_list_version"

    version_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, default=0)
    version_name = Column(String(40), nullable=False)
    list_position = Column(Integer, nullable=False, default=0)
    show_in_list = Column(Integer, nullable=False, default=0)
    version_tense = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("flyspray_project_id_version", "project_id", "version_tense"),
    )


class FlysprayNotificationMessage(Base):
    __tablename__ = "flyspray_notification_messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    message_subject = Column(Text, nullable=True)
    message_body = Column(Text, nullable=True)
    time_created = Column(Integer, nullable=False, default=0)


class FlysprayNotificationRecipient(Base):
    __tablename__ = "flyspray_notification_recipients"

    recipient_id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, nullable=False, default=0)
    notify_method = Column(String(1), nullable=False)
    notify_address = Column(String(100), nullable=False)


class FlysprayNotification(Base):
    __tablename__ = "flyspray_notifications"

    notify_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("task_id", "user_id", name="flyspray_task_id_notifs"),
    )


class FlysprayPref(Base):
    __tablename__ = "flyspray_prefs"

    pref_id = Column(Integer, primary_key=True, autoincrement=True)
    pref_name = Column(String(20), nullable=False)
    pref_value = Column(String(250), nullable=False, default="0")


class FlysprayProject(Base):
    __tablename__ = "flyspray_projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_title = Column(String(100), nullable=False)
    theme_style = Column(String(20), nullable=False, default="0")
    default_cat_owner = Column(Integer, nullable=False, default=0)
    intro_message = Column(Text, nullable=True)
    project_is_active = Column(Integer, nullable=False, default=0)
    visible_columns = Column(String(255), nullable=False)
    others_view = Column(Integer, nullable=False, default=0)
    anon_open = Column(Integer, nullable=False, default=0)
    notify_email = Column(Text, nullable=True)
    notify_jabber = Column(Text, nullable=True)
    notify_reply = Column(Text, nullable=True)
    notify_types = Column(String(100), nullable=False, default="0")
    feed_img_url = Column(Text, nullable=True)
    feed_description = Column(Text, nullable=True)
    notify_subject = Column(String(100), nullable=False, default="")
    lang_code = Column(String(10), nullable=False)
    comment_closed = Column(Integer, nullable=False, default=0)
    auto_assign = Column(Integer, nullable=False, default=0)
    last_updated = Column(Integer, nullable=False, default=0)
    default_task = Column(Text, nullable=True)
    default_entry = Column(String(8), nullable=False, default="index")


class FlysprayRegistration(Base):
    __tablename__ = "flyspray_registrations"

    reg_id = Column(Integer, primary_key=True, autoincrement=True)
    reg_time = Column(Integer, nullable=False, default=0)
    confirm_code = Column(String(20), nullable=False)
    user_name = Column(String(32), nullable=False)
    real_name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    jabber_id = Column(String(100), nullable=False)
    notify_type = Column(Integer, nullable=False, default=0)
    magic_url = Column(String(40), nullable=False)
    time_zone = Column(Integer, nullable=False, default=0)


class FlysprayRelated(Base):
    __tablename__ = "flyspray_related"

    related_id = Column(Integer, primary_key=True, autoincrement=True)
    this_task = Column(Integer, nullable=False, default=0)
    related_task = Column(Integer, nullable=False, default=0)
    is_duplicate = Column(Integer, nullable=False, default=0)

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

    reminder_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0)
    to_user_id = Column(Integer, nullable=False, default=0)
    from_user_id = Column(Integer, nullable=False, default=0)
    start_time = Column(Integer, nullable=False, default=0)
    how_often = Column(Integer, nullable=False, default=0)
    last_sent = Column(Integer, nullable=False, default=0)
    reminder_message = Column(Text, nullable=True)


class FlyspraySearch(Base):
    __tablename__ = "flyspray_searches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=0)
    name = Column(String(50), nullable=False)
    search_string = Column(Text, nullable=True)
    time = Column(Integer, nullable=False, default=0)


class FlysprayTask(Base):
    __tablename__ = "flyspray_tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, default=0)
    task_type = Column(Integer, nullable=False, default=0)
    date_opened = Column(Integer, nullable=False, default=0)
    opened_by = Column(Integer, nullable=False, default=0)
    is_closed = Column(Integer, nullable=False, default=0)
    date_closed = Column(Integer, nullable=False, default=0)
    closed_by = Column(Integer, nullable=False, default=0)
    closure_comment = Column(Text, nullable=True)
    item_summary = Column(String(100), nullable=False)
    detailed_desc = Column(Text, nullable=True)
    item_status = Column(Integer, nullable=False, default=0)
    resolution_reason = Column(Integer, nullable=False, default=1)
    product_category = Column(Integer, nullable=False, default=0)
    product_version = Column(Integer, nullable=False, default=0)
    closedby_version = Column(Integer, nullable=False, default=0)
    operating_system = Column(Integer, nullable=False, default=0)
    task_severity = Column(Integer, nullable=False, default=0)
    task_priority = Column(Integer, nullable=False, default=0)
    last_edited_by = Column(Integer, nullable=False, default=0)
    last_edited_time = Column(Integer, nullable=False, default=0)
    percent_complete = Column(Integer, nullable=False, default=0)
    mark_private = Column(Integer, nullable=False, default=0)
    due_date = Column(Integer, nullable=False, default=0)
    anon_email = Column(String(100), nullable=False, default="")
    task_token = Column(String(32), nullable=False, default="0")

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

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(32), nullable=False)
    user_pass = Column(String(40), nullable=True)
    real_name = Column(String(100), nullable=False)
    jabber_id = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    notify_type = Column(Integer, nullable=False, default=0)
    notify_own = Column(Integer, nullable=False, default=0)
    account_enabled = Column(Integer, nullable=False, default=0)
    dateformat = Column(String(30), nullable=False, default="")
    dateformat_extended = Column(String(30), nullable=False, default="")
    magic_url = Column(String(40), nullable=False, default="")
    tasks_perpage = Column(Integer, nullable=False, default=0)
    register_date = Column(Integer, nullable=False, default=0)
    time_zone = Column(Integer, nullable=False, default=0)
    login_attempts = Column(Integer, nullable=False, default=0)
    lock_until = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("user_name", name="flyspray_user_name"),
    )


class FlysprayUsersInGroup(Base):
    __tablename__ = "flyspray_users_in_groups"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=0)
    group_id = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="flyspray_group_id_uig"),
        Index("flyspray_user_id_uig", "user_id"),
    )


class FlysprayVote(Base):
    __tablename__ = "flyspray_votes"

    vote_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=0)
    task_id = Column(Integer, nullable=False, default=0)
    date_time = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("flyspray_task_id_votes", "task_id"),)
