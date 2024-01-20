"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Media(db.Model):
    """Media table"""

    __tablename__ = 'media'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    abbr = db.Column(
        db.String(5),
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    media_type = db.Column(
        db.Text,
        nullable=False,
    )

    seasons = db.Column(
        db.Integer,
        nullable=False,
    )

    ord = db.Column(
        db.Integer
    )


class Title(db.Model):
    """Title table"""

    __tablename__ = 'title'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    abbr = db.Column(
        db.String(5),
        nullable=False,
    )

    premiered_date = db.Column(
        db.Date,
        nullable=False,
    )

    media_id = db.Column(
        db.Integer,
        db.ForeignKey('media.id'),
        nullable=False,
    )

    season_id = db.Column(
        db.Integer,
        nullable=False,
    )

    episode_id = db.Column(
        db.Text,
        nullable=False,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    summary = db.Column(
        db.Text,
        nullable=True,
    )


class User(db.Model):
    """User in the system."""

    __tablename__ = 'user'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Post(db.Model):
    """Post table"""

    __tablename__ = 'post'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    abbr = db.Column(
        db.String(5),
        db.ForeignKey('title.abbr')
    )

    season_id = db.Column(
        db.Integer,
        db.ForeignKey('title.season_id')
    )

    episode_id = db.Column(
        db.Text,
        db.ForeignKey('title.episode_id')
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )


class Viewed(db.Model):
    """Viewed table"""

    __tablename__ = 'viewed'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    episode = db.Column(
        db.Text,
        nullable=False,
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
