"""This script requires the following env vars to be set
- HOST
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_PORT
- LOG_DATA_PATH
- SONG_DATA_PATH
- LOG_JSON_PATH
- IAM_ROLE_ARN
"""

from typing import List

from db_service import DBService
from settings import config


def get_load_queries() -> List[str]:
    queries = []

    # staging_songs Table
    query = f"copy staging_songs " \
            f"from '{config.SONG_DATA_PATH}' " \
            f"credentials 'aws_iam_role={config.IAM_ROLE_ARN}' " \
            f"REGION 'us-west-2'" \
            f"FORMAT AS JSON 'auto' " \
            f"TRUNCATECOLUMNS"
    queries.append(query)

    # staging_events Table
    query = f"copy staging_events " \
            f"from '{config.LOG_DATA_PATH}' " \
            f"credentials 'aws_iam_role={config.IAM_ROLE_ARN}' " \
            f"REGION 'us-west-2'" \
            f"FORMAT AS JSON '{config.LOG_JSON_PATH}' " \
            f"TRUNCATECOLUMNS " \
            f"MAXERROR 10"
    queries.append(query)

    return queries


def get_insert_queries() -> List[str]:
    queries = []

    # songplays Table
    query = f"INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) " \
            f"SELECT TIMESTAMP 'epoch' + events.ts/1000 * interval '1 second' as start_time, " \
            f"events.userId as user_id, " \
            f"events.level as level, " \
            f"songs.song_id as song_id, " \
            f"songs.artist_id as artist_id, " \
            f"events.sessionId as session_id, " \
            f"events.location as location, " \
            f"events.userAgent as user_agent " \
            f"from staging_events as events " \
            f"JOIN staging_songs as songs on events.song = songs.title " \
            f"WHERE events.page='NextSong';"
    queries.append(query)

    # users Table
    query = f"INSERT INTO users (user_id, first_name, last_name, gender, level) " \
            f"SELECT DISTINCT userId as user_id, " \
            f"firstName as first_name, " \
            f"lastName as Last_name, " \
            f"gender as gender, " \
            f"level as level " \
            f"from staging_events " \
            f"WHERE page='NextSong';"
    queries.append(query)

    # songs Table
    query = f"INSERT INTO songs (song_id, title, artist_id, year, duration) " \
            f"SELECT song_id as song_id, " \
            f"title as title, " \
            f"artist_id as artist_id, " \
            f"year as year, " \
            f"duration as duration " \
            f"from staging_songs;"
    queries.append(query)

    # artists Table
    query = f"INSERT INTO artists (artist_id, name, location, latitude, longitude) " \
            f"SELECT DISTINCT artist_id as artist_id, " \
            f"artist_name as name, " \
            f"artist_location as location, " \
            f"artist_latitude as latitude, " \
            f"artist_longitude as longitude " \
            f"from staging_songs;"
    queries.append(query)

    # time Table
    query = f"INSERT INTO time (start_time, hour, day ,week, month, year, weekday) " \
            f"SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' as start_time, " \
            f"EXTRACT(HOUR FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') as hour, " \
            f"EXTRACT(DAY FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') as month, " \
            f"EXTRACT(WEEK FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') as month, " \
            f"EXTRACT(MONTH FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') as month, " \
            f"EXTRACT(YEAR FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') as month, " \
            f"CASE WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 * interval '1 second') " \
            f"IN (6, 7) THEN false ELSE true END as weekday " \
            f"from staging_events;"
    queries.append(query)

    return queries


def main():

    db_service = DBService()

    try:
        queries = get_load_queries()
        db_service.execute_queries(queries)
    except ValueError as error:
        print(f'Error loading data: {error}')

    try:
        queries = get_insert_queries()
        db_service.execute_queries(queries)
    except ValueError as error:
        print(f'Error inserting data: {error}')

    db_service.close()


if __name__ == "__main__":
    main()
