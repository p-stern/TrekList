-- from the terminal run:
-- psql < seed.sql

DROP DATABASE IF EXISTS startrek;

CREATE DATABASE startrek;

\c startrek

CREATE TABLE media (
    id SERIAL   NOT NULL,
    abbr text   NOT NULL,
    name text   NOT NULL,
    media_type text   NOT NULL,
    ord int   NOT NULL,
    CONSTRAINT pk_media PRIMARY KEY (
        id
     )
);

INSERT INTO media
  (id, abbr, name, media_type, ord)
VALUES
(1, 'Movie', 'Movie', 'Movie', 1),
(490, 'TOS', 'Star Trek', 'TV', 2),
(3513, 'TAS', 'Star Trek: The Animated Series', 'TV', 3),
(491, 'TNG', 'Star Trek: The Next Generation', 'TV', 4),
(493, 'DS9', 'Star Trek: Deep Space Nine', 'TV', 5),
(492, 'VOY', 'Star Trek: Voyager', 'TV', 6),
(714, 'ENT', 'Star Trek: Enterprise', 'TV', 7),
(7480, 'DIS', 'Star Trek: Discovery', 'TV', 8),
(39744, 'ST', 'Star Trek: Short Treks', 'TV', 9),
(42193, 'PIC', 'Star Trek: Picard', 'TV', 10),
(39323, 'LD', 'Star Trek: Lower Decks', 'TV', 11),
(49333, 'PRO', 'Star Trek: Prodigy', 'TV', 12),
(48090, 'SNW', 'Star Trek: Strange New Worlds', 'TV', 13);


CREATE TABLE "title" (
    "id" SERIAL   NOT NULL,
    "abbr" text   NOT NULL,
    "premiered_date" date   NOT NULL,
    "media_id" int   NOT NULL,
    "season_id" int   NOT NULL,
    "episode_id" text   NOT NULL,
    "title" text   NOT NULL,
    "summary" text,
    CONSTRAINT "pk_title" PRIMARY KEY (
        "id"
     )
);

INSERT INTO title
  (id, abbr, premiered_date, media_id, season_id, episode_id, title, summary)
VALUES
  (1, 'Movie', '1979-12-07', 1, 1, '1', 'Star Trek: The Motion Picture', ' '),
  (2, 'Movie', '1982-06-04', 1, 1, '2', 'Star Trek II: The Wrath of Khan', ' '),
  (3, 'Movie', '1984-06-01', 1, 1, '3', 'Star Trek III: The Search for Spock', ' '),
  (4, 'Movie', '1986-11-26', 1, 1, '4', 'Star Trek IV: The Voyage Home', ' '),
  (5, 'Movie', '1989-06-09', 1, 1, '5', 'Star Trek V: The Final Frontier', ' '),
  (6, 'Movie', '1991-12-06', 1, 1, '6', 'Star Trek VI: The Undiscovered Country', ' '),
  (7, 'Movie', '1994-11-18', 1, 2, '1', 'Star Trek Generations', ' '),
  (8, 'Movie', '1996-11-22', 1, 2, '2', 'Star Trek: First Contact', ' '),
  (9, 'Movie', '1998-12-11', 1, 2, '3', 'Star Trek: Insurrection', ' '),
  (10, 'Movie', '2002-12-13', 1, 2, '4', 'Star Trek Nemesis', ' '),
  (11, 'Movie', '2009-05-08', 1, 3, '1', 'Star Trek', ' '),
  (12, 'Movie', '2013-05-16', 1, 3, '2', 'Star Trek Into Darkness', ' '),
  (13, 'Movie', '2016-07-22', 1, 3, '3', 'Star Trek Beyond', ' ');


-- Get Max ID from title
SELECT MAX(id) FROM title;

-- Get Next ID from title
SELECT nextval('title_id_seq');

-- Set Next ID Value to MAX ID
SELECT setval('title_id_seq', (SELECT MAX(id) FROM title));

CREATE INDEX premiered_index ON title (premiered_date);

CREATE TABLE "user" (
    "id" SERIAL   NOT NULL,
    "username" text   NOT NULL,
    "password" text   NOT NULL,
    CONSTRAINT "pk_user" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "post" (
    "id" SERIAL   NOT NULL,
    "user_id" int   NOT NULL,
    "title_id" int   NOT NULL,
    "title" text   NOT NULL,
    "content" text   NOT NULL,
    "created_at" timestamp   NOT NULL,
    CONSTRAINT "pk_post" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "viewed" (
    "id" SERIAL   NOT NULL,
    "user_id" int   NOT NULL,
    "title_id" int   NOT NULL,
    CONSTRAINT "pk_viewed" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "title" ADD CONSTRAINT "fk_title_media_id" FOREIGN KEY("media_id")
REFERENCES "media" ("id");

ALTER TABLE "post" ADD CONSTRAINT "fk_post_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "post" ADD CONSTRAINT "fk_post_title_id" FOREIGN KEY("title_id")
REFERENCES "title" ("id");

ALTER TABLE "viewed" ADD CONSTRAINT "fk_viewed_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "viewed" ADD CONSTRAINT "fk_viewed_title_id" FOREIGN KEY("title_id")
REFERENCES "title" ("id");
