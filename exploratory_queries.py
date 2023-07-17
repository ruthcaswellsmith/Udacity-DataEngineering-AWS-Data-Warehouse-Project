"""This script requires the following env vars to be set
- HOST
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_PORT
"""

from db_service import DBService


def main():

    db_service = DBService()
    queries = [
        f'select users.gender, count(songplay_id) as num_plays from songplays '
        f'join users on users.user_id = songplays.user_id '
        f'group by users.gender;',

        f'select songs.title, count(songplay_id) as num_plays from songplays '
        f'join songs on songs.song_id = songplays.song_id '
        f'group by songs.title '
        f'order by num_plays desc limit 10;',

        f'select weekday, avg(songs_per_day) as songs_per_day '
        f'from ( '
        f'  select songplays.user_id, time.day, count(songplays.songplay_id) as songs_per_day, time.weekday '
        f'  from songplays '
        f'  join time on time.start_time = songplays.start_time'
        f'  group by user_id, day, weekday '
        f') subquery '
        f'group by weekday;',

        f'select hour, avg(songs_per_hour) as songs_per_hour '
        f'from ( '
        f'  select user_id, hour, count(songplay_id) as songs_per_hour '
        f'  from songplays '
        f'  join time on time.start_time = songplays.start_time '
        f'  group by user_id, hour '
        f') subquery '
        f'group by hour '
        f'order by songs_per_hour desc;'
    ]

    for query in queries:
        db_service.execute_query(query)
        print(f"\n{query}")
        print(db_service.cur.fetchall())

    db_service.close()


if __name__ == "__main__":
    main()
