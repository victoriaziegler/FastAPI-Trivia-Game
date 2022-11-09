import os
from psycopg_pool import ConnectionPool

user = os.environ["PGUSER"]
password = os.environ["PGPASSWORD"]
db = os.environ["PGDATABASE"]
host = os.environ["PGHOST"]

db_url = f'postgresql://{user}:{password}@{host}/{db}'

pool = ConnectionPool(conninfo=db_url)


class CategoryQueries:
    # THIS IS WORKING
    def get_all_categories(self, num_results=100):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                query = ("""
                    SELECT id, title, canon
                    FROM categories
                """)

                if num_results and type(num_results) == int:
                    query += f"LIMIT {num_results}"
                cur.execute(query)

                results = []
                for row in cur.fetchall():
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                    results.append(record)
                return results

    # def get_n_categories(self, num_results=N*100):
    #     with pool.connection() as conn:
    #         with conn.cursor() as cur:
    #             query = ("""
    #                 SELECT id, title, canon
    #                 FROM categories
    #             """)

    #             if num_results and type(num_results) == int:
    #                 query += f"LIMIT {num_results} OFFSET %N"
    #             cur.execute(query)

    #             results = []
    #             for row in cur.fetchall():
    #                 record = {}
    #                 for i, column in enumerate(cur.description):
    #                     record[column.name] = row[i]
    #                 results.append(record)
    #             return results

    def get_category(self, category_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, canon
                    FROM categories
                    WHERE id = %s
                    """,
                        [category_id],
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

                return record

    def create_category(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.title,
                    data.canon,
                ]
                cur.execute(
                    """
                    INSERT INTO categories (title, canon)
                    VALUES (%s, %s)
                    RETURNING category_id, title, canon
                    """,
                    params,
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

    def update_category(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.title,
                    data.canon,
                ]
                cur.execute(
                    """
                    UPDATE categories
                    SET title = %s,
                        canon = %s
                    WHERE category_id = %s
                    RETURNING category_id, title, canon
                    """,
                    params,
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

                return record

# THIS WONT WORK FOR LOW NUMBERS BUT WORKED FOR A REALLY HIGH NUMBER???? FK ISSUE
    def delete_category(self, id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM categories
                    WHERE id = %s
                    """,
                    [id],
                )