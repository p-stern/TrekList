import os
from pdb import Pdb
from pyexpat.errors import messages

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import json

import requests
from datetime import date, datetime

from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db, Media, Title, User, Post, Viewed

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get(('DATABASE_URL').replace("://", "ql://", 1)), 'postgresql:///startrek')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def get_viewed(user):
    """Get viewed episodes for user"""

    viewed = Viewed.query.filter(
        Viewed.user_id == user.id).order_by(Viewed.id).all()
    return viewed


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    return


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    do_logout()
    flash("User logged out.", 'success')
    return redirect("/login")


##############################################################################
# Messages routes:

@app.route('/messages/<int:title_id>', methods=["GET", "POST"])
def messages_show(title_id):
    """Show a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MessageForm()

    title, media = db.session.query(Title, Media).join(Media, Media.id == Title.media_id).filter(
        Title.id == title_id).first()

    if form.validate_on_submit():
        post = Post(user_id=g.user.id, title_id=title_id,
                    title="", content=form.text.data)
        db.session.add(post)
        db.session.commit()
        form.text.data = ""

    posts = db.session.query(Post, User).join(
        User, User.id == Post.user_id).filter(Post.title_id == title_id).order_by(
        Post.created_at).all()

    # Format date/time for message display
    for post in posts:
        post.Post.created_at = post.Post.created_at.strftime(
            "%d %B %Y, %H:%M:%S")

    return render_template('messages/post.html', title=title, media=media, posts=posts, form=form)


##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage"""
    today = date.today()

    media = Media.query.order_by(Media.ord).all()

    if g.user:
        titles = db.session.query(Title, Media, db.func.count(Post.id).label("comment_count")).join(Media).join(Post, Post.title_id == Title.id, isouter=True).group_by(Title.id, Media.id).order_by(
            Title.premiered_date, Media.ord, Title.season_id, Title.episode_id).all()
    else:
        titles = Title.query.join(Media).order_by(
            Title.premiered_date, Media.ord, Title.season_id, Title.episode_id).all()

    movies = Title.query.filter(Title.abbr == "Movie").order_by(
        Title.season_id, Title.episode_id).all()

    if g.user:
        viewed = get_viewed(g.user)
        viewed_list = []
        for v in viewed:
            viewed_list.append(v.episode)

        return render_template('home.html', media=media, titles=titles, movies=movies, today=today, viewed=viewed_list)
    else:
        return render_template('home-anon.html', media=media, titles=titles, movies=movies, today=today)


##############################################################################
# Episodes


@app.route('/episodes', methods=["POST"])
def episodes():
    """Post episodes"""

    # get episodes dict
    episode_dict = request.get_json()

    # convert episodes dict to list
    episodes = json.loads(episode_dict["episodes"])

    Viewed.query.filter_by(user_id=g.user.id).delete()

    db.session.commit()

    for episode in episodes:
        viewed = Viewed(
            user_id=g.user.id,
            episode=episode,
        )

        db.session.add(viewed)

    db.session.commit()
    return '1'


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask


@ app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
