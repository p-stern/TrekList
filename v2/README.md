# TrekList - a Guide to Star Trek television shows and films #
##

## Deployed on Railway ##

[https://treklist-production.up.railway.app/](https://treklist-production.up.railway.app/ "TrekList")
## Description ##

TrekList lists Star Trek episodes and movies in the order they were released.  

## Features ##


- Series, Season/Episode, Title and Airdate is listed for each entry.

- Each Title links to a description on the Memory Alpha site, [https://memory-alpha.fandom.com/wiki/Portal:Main
](https://memory-alpha.fandom.com/wiki/Portal:Main "Memory Alpha")

- (Optional) Sign up

	- Click Sign Up and add username and password to register.
	
	- Signing up unlocks additional features
	
		- Checkboxes for Movies and Television Seasons will be displayed in the legend on the left of the main list.
		- Checkboxes will be displayed next to each individual episode
		- Check the  checkboxes by season or for individual episodes and movies to keep track of which have been watched
		- Total Episodes Watched to the right of the main list will be incremented to display a watched count. 
		- A comment feature is enabled to comment on individual episodes.  An episode that contains comments will display a solid comment icon while an episode that does not contain comments will display an outlined comment icon.  Clicking on either icon will redirect to the message page for the episode.

## APIs ##

The TrekList data comes from the TVMAZE API, [https://www.tvmaze.com/api](https://www.tvmaze.com/api "TVMAZE API")

## Technology Stack ##

- HTML
- CSS
- Bcrypt for passwords
- Python
- Flask
- Javascript
- SQLALchemy
- PostgreSQL


## Schema ##

>	
	media
	-
	id pk SERIAL
	abbr text
	name text
	media_type text
	seasons int
	ord int
>
	title
	-
	id pk SERIAL
	abbr text
	premiered_date date
	media_id int FK >- media.id
	season_id int
	episode_id int
	title text
	summary text
>	
	user
	-
	id pk SERIAL
	username text
	password text
>	
	post
	-
	id pk SERIAL
	user_id  int FK >- user.id
	media_id int FK >- title.media_id
	season_id int FK >- title.season_id
	episode_id int FK >- title.episode_id
	title text
	content text
	created_at timestamp
>	
	viewed
	-
	id pk SERIAL
	user_id  int FK >- user.id
	episode text

