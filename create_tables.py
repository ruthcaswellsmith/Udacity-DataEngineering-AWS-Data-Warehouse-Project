"""This script requires the following env vars to be set
- HOST
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_PORT
"""

from typing import List

from db_service import DBService
from table_config import TABLES


def get_drop_queries() -> List[str]:
    queries = []
    for table in TABLES:
        queries.append(f"DROP TABLE IF EXISTS {table.name};")
    return queries


def get_create_queries() -> List[str]:
    queries = []
    for table in TABLES:
        query = f"CREATE TABLE {table.name} ("
        cols = []
        for column in table.columns:
            col = f"{column.name} {column.datatype}"
            if column.not_null:
                col += " NOT NULL"
            if column.sort_key:
                col += " SORTKEY"
            if column.dist_key:
                col += " DISTKEY"
            cols.append(col)
        query += f"{', '.join(cols)})"
        if table.dist_style:
            query += f" DISTSTYLE {table.dist_style}"
        query += ";"

        queries.append(query)
    return queries


def main():

    db_service = DBService()

    try:
        queries = get_drop_queries()
        db_service.execute_queries(queries)
    except Exception as error:
        print(f'Error dropping table: {error}')

    try:
        queries = get_create_queries()
        db_service.execute_queries(queries)
    except Exception as error:
        print(f'Error creating table: {error}')

    db_service.close()


if __name__ == "__main__":
    main()
