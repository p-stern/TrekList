import os
from pdb import Pdb
from pyexpat.errors import messages

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import json

import requests
from datetime import date

from models import db, connect_db, Media, Title, User, Post, Viewed

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///startrek'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage"""
    today = date.today()

    media = Media.query.order_by(Media.ord).all()
    Title.query.filter(Title.media_id != 1).delete()
    db.session.commit()

    misnamed_episodes = ["Encounter at Farpoint (2)", "Emissary, Part II", "All Good Things... (2)", "Caretaker, Part II", "The Way of the Warrior, Part II",  "Dark Frontier, Part II",
                         "What You Leave Behind, Part II", "Flesh and Blood, Part II", "Endgame, Part II", "Broken Bow (2)"]

    for m in media:                  # Retrieve episodes for each TV Series and insert into 'title' table
        if m.media_type == 'TV':     # Do not include Movies
            url = "http://api.tvmaze.com/shows/" + str(m.id) + "/episodes"
            res = requests.get(url)
            data = res.json()
            for d in data:
                abbr, season, name, episode = corrections(
                    m.abbr, d['season'], d['name'], d['number'])
                if name not in misnamed_episodes:
                    title = Title(abbr=m.abbr, premiered_date=d['airdate'], media_id=m.id,
                                  season_id=d['season'], episode_id=episode, title=name, summary=d['summary'])
                    db.session.add(title)
                    db.session.commit()

            titles = Title.query.join(Media).order_by(
                Title.premiered_date, Media.ord, Title.season_id, Title.episode_id).all()

    return render_template('home-anon.html', media=media, titles=titles, today=today)


def corrections(abbr, season, name, episode):
    """Tweak titles so that the a href points to an existing url"""

    # TOS
    if name == "What Are Little Girls Made of?":
        name = "What Are Little Girls Made Of?"

    if name == "The Menagerie (1)":
        name = "The Menagerie, Part I"

    if name == "The Menagerie (2)":
        name = "The Menagerie, Part II"

    if name == "Operation: Annihilate!":
        name = "Operation -- Annihilate!"

    # TAS

    if name == "How Sharper Than a Serpent's Tooth?":
        name = "How Sharper Than a Serpent's Tooth"

    # TNG

    if name == "Encounter at Farpoint (1)":
        name = "Encounter at Farpoint"
        episode = "1/2"

    if name == "Loud as a Whisper":
        name = "Loud As A Whisper"

    if name == "The Measure of a Man":
        name = "The Measure Of A Man"

    if name == "Q Who?":
        name = "Q Who"

    if name == "Up the Long Ladder":
        name = "Up The Long Ladder"

    if name == "Who Watches the Watchers":
        name = "Who Watches The Watchers"

    if name == "The Best of Both Worlds Part II":
        name = "The Best of Both Worlds, Part II"

    if name == "I, Borg":
        name = "I Borg"

    if name == "All Good Things... (1)":
        name = "All Good Things..."
        episode = "25/26"

    # DS9

    if name == "Emissary, Part I":
        name = "Emissary"
        episode = "1/2"

    # VOY

    if name == "Caretaker, Part I":
        name = "Caretaker"
        episode = "1/2"

    if name == "The Way of the Warrior, Part I":
        name = "The Way of the Warrior"
        episode = "1/2"

    if name == "...Nor the Battle to the Strong":
        name = "Nor the Battle to the Strong"

    if name == "Future's End, Part I":
        name = "Future's End"

    if name == "Scorpion, Part I":
        name = "Scorpion"

    if name == "Year of Hell, Part I":
        name = "Year of Hell"

    if name == "The Killing Game, Part I":
        name = "The Killing Game"

    if name == "Dark Frontier, Part I":
        name = "Dark Frontier"
        episode = "15/16"

    if name == "Equinox, Part I":
        name = "Equinox"

    if name == "What You Leave Behind, Part I":
        name = "What You Leave Behind"
        episode = "25/26"

    if name == "Tinker, Tenor, Doctor, Spy":
        name = "Tinker Tenor Doctor Spy"

    if name == "Unimatrix Zero, Part I":
        name = "Unimatrix Zero"

    if name == "Flesh and Blood, Part I":
        name = "Flesh and Blood"
        episode = "9/10"

    if name == "Workforce, Part I":
        name = "Workforce"

    if name == "Endgame, Part I":
        name = "Endgame"
        episode = "25/26"

    # ENT

    if name == "Broken Bow (1)":
        name = "Broken Bow"
        episode = "1/2"

    if name == "Shockwave (1)":
        name = "Shockwave"

    if name == "Shockwave (2)":
        name = "Shockwave, Part II"

    if name == "Storm Front (1)":
        name = "Storm Front"

    if name == "Storm Front (2)":
        name = "Storm Front, Part II"

    if name == "Babel One (1)":
        name = "Babel One"

    if name == "United (2)":
        name = "United"

    if name == "The Aenar (3)":
        name = "The Aenar"

    if name == "Affliction (1)":
        name = "Affliction"

    if name == "Divergence (2)":
        name = "Divergence"

    if name == "In a Mirror, Darkly (1)":
        name = "In a Mirror, Darkly"

    if name == "In a Mirror, Darkly (2)":
        name = "In a Mirror, Darkly, Part II"

    # DIS

    if name == "The War Without, the War Within":
        name = "The War Without, The War Within"

    if name == "Such Sweet Sorrow, Part 1":
        name = "Such Sweet Sorrow"

    if name == "…But to Connect":
        name = "...But to Connect"

    if name == "Ghost of Illyria":
        name = "Ghosts of Illyria"

    # PRO

    if abbr == "PRO" and season == 1:
        if name == "Lost and Found":
            episode = "1/2"
        else:
            episode = episode + 1

    return abbr, season, name, episode

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
