from app import db
from flask_login import UserMixin
import enum
from sqlalchemy.sql import func
import enum



class UserRole(enum.Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'


class AuditMixin:
    __abstract__ = True

    created_by = db.Column(db.String(150), nullable=False)
    modified_by = db.Column(db.String(150), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modified_date = db.Column(db.DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class User(db.Model, UserMixin, AuditMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.MANAGER, nullable=False)



