# Multinational Retail Data Centralisation

The intention of this project is to centralise, clean up, and find "the ultimate truth" from a number of disparate and human-maintained databases scattered about a fictional company's server estate. The data contains errors and omissions, and is organised based on the designs of several different authors. The first stages are to gather all this information into a new master database, and to remove any errors during this process. The second phase is to then use SQL commands to query the data for basic answers. These SQL queries could be built into live reports, or simply a powerpoint to be sent to management - but this phase is not addressed.

This is an example project from the AICore curriculum, intended to teach the basic concepts of data manipulation & give candidates a taste of Data Analytics. The project is composed of milestones to building the functional code, these will be described first, before the full functionality is outlined.

# Milestones 1 & 2

Getting everything in place

 - Read source database in RDS
 - Read pdfs with supplementary data
 - Clean incoming data based on context
	 - for this I've created Jupyter Notebooks to explore the different data, try different methods and then applied the most successful/relevant into the main codebase
 - Store cleaned data in local postgressql database.

 # Milestones 3 & 4

These were undertaken on a local postgresql server, and so there's very little reflection of them here on github. The steps were as follows:

- Clean SQL tables
	- Specify column types
	- Add keys
	- Add foreign keys

- Query SQL tables
	- the most complex of these queries are saved in big_sql_queries.txt for posterity.
