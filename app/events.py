from flask import has_request_context
from flask_login import current_user
from sqlalchemy import event
from datetime import datetime, timezone
from app import db
from datetime import datetime

def get_current_username():
    if has_request_context() and current_user.is_authenticated:
        return f"{current_user.first_name} {current_user.last_name}"
    return 'system'


@event.listens_for(db.Model, 'before_insert', propagate=True)
def set_created_updated(mapper, connection, target):
    now = datetime.now(timezone.utc)
    target.created_date = now
    target.modified_date = now
    if hasattr(target, 'created_by') and not getattr(target, 'created_by', None):
        target.created_by = get_current_username()
    if hasattr(target, 'modified_by'):
        target.modified_by = get_current_username()


@event.listens_for(db.Model, 'before_update', propagate=True)
def set_updated(mapper, connection, target):
    target.modified_date = datetime.now(timezone.utc)
    if hasattr(target, 'modified_by'):
        target.modified_by = get_current_username()