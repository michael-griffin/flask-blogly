"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


DEFAULT_IMAGE_URL = '/static/default-image.jpg'

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User documentation"""
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(30),
        nullable=False)

    last_name = db.Column(
        db.String(30),
        nullable=False)

    image_url = db.Column(
        db.String(),
        nullable=True,
        default=DEFAULT_IMAGE_URL)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post column setup"""
    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.Date(),
        default=datetime.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        # nullable=False,
    )

    user = db.relationship('User', backref="posts")

