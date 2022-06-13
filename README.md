# TrekList

The Trek List will display a list of episodes spanning 11 television series and 13 films (so far) from the Star Trek franchise in order of airdate or date of movie release.

1.	What goal will your website be designed to achieve?
The purpose of this list is purely informational.  A list of this type would allow fans to assess how much they have watched or what to watch next.

2.	What kind of users will visit your site? In other words, what is the demographic of
your users?  
This would appeal to a demographic of all ages who enjoy Star Trek and want to see a timeline of the series.

3.	What data do you plan on using? You may have not picked your actual API yet,
which is fine, just outline what kind of data you would like it to contain.

	API options:
	
	     •	STAPI http://stapi.co/
	
	     •	TVMAZE API https://www.tvmaze.com/api
	
	     •	IMDB API https://imdb-api.com/
	
	Data that would be needed are a list of series/movies, and a list of episodes with airdates.  While STAPI is a Star Trek specific API, it may not be user friendly and the data may not be current.  If this is the case, TVMAZE API could be used to retrieve television information together with IMDB API for movie information.


4.	In brief, outline your approach to creating your project (knowing that you may not
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:

      a. What does your database schema look like?

    Two tables are initially required:

   	 1) List of Series & Movies

  	 2) List of Episodes/Movies with respective airdate/release date.
     
      The tables could be loaded with the data from the API(s) and then queried in airdate order to load the page.

      b. What kinds of issues might you run into with your API?
      STAPI might not contain current data and also may require a learning curve based on the documentation.

      c. Is there any sensitive information you need to secure?
      A stretch goal to add register/login credentials may need to secure a password.

      d. What functionality will your app include?
      This will be a read-only list.  Stretch goals could increase the functionality.

      e. What will the user flow look like?
      The user would see a list of series as well as an episode list.  Additionally, clicking on a series in the series list would take the user to the point       in the episode list where the series is first listed.

      f. What features make your site more than CRUD? Do you have any stretch goals?

      1)	The episode list could contain hyperlinks to episode synopses on the Memory Alpha (https://memory-alpha.fandom.com/wiki/Portal:Main) site

      2)	By adding register/login logic, a user could mark the episodes they have already seen.

      3)  Registered users could add comments to episodes
