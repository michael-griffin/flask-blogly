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




class Tag(db.Model):
    """Tag links a post and a tag together. Each post can only be assigned to
    a tag one time."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    posts = db.relationship('Post', secondary="post_tags", backref="tag")



class PostTag(db.Model):
    """Through table for Post and Tag"""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True,
        nullable=False,
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True,
        nullable=False,
    )
