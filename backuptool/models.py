from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Saves User Infos and Credentials

    ID = Autoincrement (Primary_Key)
    Username = User-chosen unique username
    Password = Argon2 hash
    Email = User's Email used for notifications
    Role = [admin (can do everything), user (can create schedules, backups, ...), viewer (readonly)]
    Created At = When the user was created (makes stuff simpler)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(16), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Setting(db.Model):
    """
    Saves Global settings. (Key-Value)
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=True)
