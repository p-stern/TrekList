import time
import requests
import os
from models import db, connect_db, Media, Title
from flask import Flask

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///startrek'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)


def populate_db():
    Title.query.filter(Title.media_id != 1).delete()
    db.session.commit()
    print("Title table deleted")

    misnamed_episodes = ["Encounter at Farpoint (2)", "Emissary, Part II", "All Good Things... (2)", "Caretaker, Part II", "The Way of the Warrior, Part II",  "Dark Frontier, Part II",
                         "What You Leave Behind, Part II", "Flesh and Blood, Part II", "Endgame, Part II", "Broken Bow (2)"]

    media = Media.query.order_by(Media.ord).all()
    for m in media:                  # Retrieve episodes for each TV Series and insert into 'title' table
        if m.media_type == 'TV':     # Do not include Movies
            url = "http://api.tvmaze.com/shows/" + str(m.id) + "/episodes"
            res = requests.get(url)
            data = res.json()
            for d in data:
                season, name, episode, airdate = corrections(
                    m.abbr, d['season'], d['name'], d['number'], d['airdate'])
                if name not in misnamed_episodes:
                    add_title(m.abbr, airdate, m.id, season,
                              episode, name, d['summary'])

    addSpecialEpisode(m)

    db.session.commit()
    print("Loaded")
    return schedule.CancelJob


def add_title(abbr, airdate, id, season, episode, name, summary):
    title = Title(abbr=abbr, premiered_date=airdate, media_id=id,
                  season_id=season, episode_id=episode, title=name, summary=summary)
    db.session.add(title)


def addSpecialEpisode(m):
    """Get Pilot episode (which has episode None)"""

    url = "http://api.tvmaze.com/seasons/1921/episodes"

    res = requests.get(url)
    data = res.json()
    for d in data:
        if d['number'] == None:
            season, name, episode, airdate = corrections(
                m.abbr, d['season'], d['name'], d['number'], d['airdate'])
            add_title('TOS', airdate, 490, season, episode, name, d['summary'])


def corrections(abbr, season, name, episode, airdate):
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

    if name == "The Cage (Pilot)":
        name = "The Cage"
        season = 0
        episode = 0
        airdate = '1988-10-04'

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

    if name == "The Way of the Warrior, Part I":
        name = "The Way of the Warrior"
        episode = "1/2"

    if name == "Let He Who is Without Sin...":
        name = "Let He Who Is Without Sin..."

    # VOY

    if name == "Caretaker, Part I":
        name = "Caretaker"
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

    if name == "Demons (1)":
        name = "Demons"

    if name == "Terra Prime (2)":
        name = "Terra Prime"

    # DIS

    if name == "The War Without, the War Within":
        name = "The War Without, The War Within"

    if name == "Such Sweet Sorrow, Part 1":
        name = "Such Sweet Sorrow"

    if name == "There Is a Tide…":
        name = "There Is A Tide..."

    if name == "…But to Connect":
        name = "...But to Connect"

    # SNW

    if name == "Ghost of Illyria":
        name = "Ghosts of Illyria"

    # PRO

    if abbr == "PRO" and season == 1:
        if name == "Lost and Found":
            episode = "1/2"
        else:
            episode = episode + 1

    return season, name, episode, airdate


populate_db()
