"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


DEFAULT_IMAGE_URL = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fvectors%2Fblank-profile-picture-mystery-man-973460%2F&psig=AOvVaw2mtXUjpMufpUsZF82k5snm&ust=1693519676240000&source=images&cd=vfe&opi=89978449&ved=0CA8QjRxqFwoTCLiEwceyhYEDFQAAAAAdAAAAABAE'


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
