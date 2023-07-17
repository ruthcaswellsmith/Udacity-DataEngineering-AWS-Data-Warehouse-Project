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
        'select count(*) from staging_songs',
        'select count(*) from staging_events',
        'select count(*) from songplays',
        'select count(*) from users',
        'select count(*) from songs',
        'select count(*) from artists',
        'select count(*) from time'
    ]
    for query in queries:
        db_service.execute_query(query)
        print(f"\n{query}")
        print(db_service.cur.fetchall())

    db_service.close()


if __name__ == "__main__":
    main()
