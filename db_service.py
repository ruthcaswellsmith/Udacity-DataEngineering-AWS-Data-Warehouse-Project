from typing import List

import psycopg2

from settings import config


class DBService:

    def __init__(self):
        self.conn = psycopg2.connect(f"host={config.HOST} "
                                     f"dbname={config.DB_NAME} "
                                     f"user={config.DB_USER} "
                                     f"password={config.DB_PASSWORD} "
                                     f"port={config.DB_PORT}")
        self.cur = self.conn.cursor()

    def execute_queries(self, queries: List[str]):
        for query in queries:
            print(f"Executing {query}")
            self.cur.execute(query)
            self.conn.commit()

    def execute_query(self, query: str):
        self.cur.execute(query)
        return self.cur

    def close(self):
        self.conn.close()
