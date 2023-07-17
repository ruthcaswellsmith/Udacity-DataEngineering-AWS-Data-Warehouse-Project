"""This script requires the following env vars to be set
- HOST
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_PORT
"""

from db_service import DBService


def main(query: str):

    db_service = DBService()

    db_service.execute_query(query)
    print(db_service.cur.fetchall())

    db_service.close()


if __name__ == "__main__":
    input_query = input("Enter the SQL query: ")
    main(input_query)
