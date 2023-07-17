## Data Warehouse Project
#### Udacity Data Engineering in AWS
#### Ruth Caswell Smith

### Context

The Redshift database is designed to allow business users of Sparkify to understand song plays.
Raw data is loaded from both event data (i.e. instances of song plays) and song data (i.e. data
about individual songs). The raw data is loaded into staging tables, then inserted into a star
schema optimized for business analysis queries.

### Database Design
There are staging tables:
 - event (log) data
 - song data

The columns in these tables correspond 1-1 with the fields in the raw json files.

There is a single fact table:
- songplays

This table contains information on each songplay, as filtered from the event data based on
the "page" attribute being equal to "NextSong".  This table contains an automatically
generated id, as well as id's corresponding to the dimension tables (detailed below)
as well as some additional fields such as location and user agent (browser information).
It is populated by a join on the event and song data an song title.  Because of this
required join, the two tables are created with the song title as a distribution key.

There are four dimension tables:
- time (distinct entries from event staging table)
- user (distinct entries from event staging table)
- song (entries from the song staging table joined with the song staging table)
- artist (distinct entries from the song staging table)

Each of these contains an id as well as additional information about each entry.

To optimize query performance, the dimension tables for artist and user are distributed to
all nodes, since they are smaller and this can be increase query performance.  The song
and time dimension tables, since they are large, are distributed across all nodes.

Since my expectation is that the song dimension table will be joined frequently with the
song table, and the song table is distributed across all nodes, I have set song_id to be a
distribution key for both the songplays fact table and the songs dimension table.
In addition I have set a few keys to be sort keys in order to optimized query performance,
but have not set too many as setting too many sort keys can reduce overall performance.
I have chosen the primary key from each of the dimension tables to be a sort key, and for the
fact table I have chosen start time to be a sort key.


### Confirmation of ETL pipeline
Because I was running into extremely long query times for the COPY commands (please see this thread
 https://knowledge.udacity.com/questions/997131, I ended up only loading songs parititoned by the
letter 'B' and events from 2018/11.

> select count(*) from staging_songs
[(14541,)]

> select count(*) from staging_events
[(8056,)]

> select count(*) from songplays
[(1079,)]

> select count(*) from users
[(104,)]

> select count(*) from songs
[(14541,)]

> select count(*) from artists
[(9693,)]

> select count(*) from time
[(8056,)]

### Sample Queries
Below are some sample queries I ran on the data.

> Which gender is using the service more?

>select users.gender, count(songplay_id) as num_plays from songplays join users on users.user_id = songplays.user_id group by users.gender

>[('M', 426), ('F', 1150)]


> What were the 10 most popular songs?

>select songs.title, count(songplay_id) as num_plays from songplays join songs on songs.song_id = songplays.song_id group by songs.title order by num_plays desc limit 10

>[('Intro', 63), ('Home', 52), ("You're The One", 37), ('Fireflies', 28), ('Rain', 12), ('Yellow', 12), ('Hold On', 12), ('Gone', 12), ('Forever', 12), ('Wake Up', 10)]


> Are more songs played on average by users on weekends or weekdays?

>select weekday, avg(songs_per_day) as songs_per_day from (   select songplays.user_id, time.day, count(songplays.songplay_id) as songs_per_day, time.weekday   from songplays   join time on time.start_time = songplays.start_time  group by user_id, day, weekday ) subquery group by weekday

>[(True, 4), (False, 3)]


> What is the busiest hour of the day?

>select hour, avg(songs_per_hour) as songs_per_hour from (   select user_id, hour, count(songplay_id) as songs_per_hour   from songplays   join time on time.start_time = songplays.start_time   group by user_id, hour ) subquery group by hour order by songs_per_hour desc;

>[(22, 5), (5, 4), (18, 4), (9, 3), (19, 3), (17, 3), (10, 3), (15, 3), (16, 3), (23, 3), (20, 3), (11, 3), (6, 2), (14, 2), (7, 2), (12, 2), (4, 2), (8, 2), (13, 2), (3, 1), (21, 1), (2, 1), (0, 1), (1, 1)]


### Running this Project
This project uses pydantic BaseSettings to manage environment variables.  To install and run in PyCharm:
- clone the repo
- create a new a project
- from Terminal pip install -r requirements.txt
- set up a run configuration for each script below with environment variables as specified in
the top of each file.  *Note not all environment variables are required for every script.*

#### Infrastructure as code
- create_iam_role.py - creates an IAM role for the redshift cluster to access S3
- open_tcp_port.py - opens a TCP port for the cluster
- create_cluster.py - creates a redshift cluster and database using env variables
- get_cluster_status.py - gets the status of a cluster
- delete_cluster.py - deletes a cluster

#### Connecting to, Creating, and Populating Database
- create_tables.py - drops and then creates all tables as specified in table_config.py
- etl.py - runs the copy commands to create the staging tables and the insert commands to populate the
star schema

#### Queries
- confirm_etl_pipeline.py - gets row counts for all tables, both staging and star schema tables
- adhoc_query.py - allows user to enter an adhoc query of the database and returns all results.
- exploratory_queries.py - executes some sample queries for this project submission.

*Note that all scripts interacting with the database use the common service db_service.py which is responsible
for managing the connection and executing queries.*

### Challenges / Future improvements:
- Originally my cluster was in us-east-1 while the S3 bucket was in us-west-2. This made the
COPY command extremeley slow.
- I realized that for testing purposes only a single partition of the data should be copied to speed
up the copy commands
- I ran into a lot of issues with varchar fields overflowing.  I ended up increasing most of
my fields but also truncated the raw data.
- I ran into issues with the unix timestamp.  It was tricky to figure out how to load it
and how to transform it correctly.
- I wanted to ignore fields in the event data that I did not require in the star schema, but that
would require rewriting the json format file and I wasn't sure how much it would improve performance.
Something to consider in the future.
- I investigated the idea of filtering the event data, so that only data for which
page="NextSong" was copied, but this is not currently possible with the Redshift COPY command.
- further analysis and benchmarking of typical queries could be done in order to determine which
columns should be set as sort keys.




