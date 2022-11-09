import os
from psycopg_pool import ConnectionPool

user = os.environ["PGUSER"]
password = os.environ["PGPASSWORD"]
db = os.environ["PGDATABASE"]
host = os.environ["PGHOST"]

db_url = f'postgresql://{user}:{password}@{host}/{db}'

pool = ConnectionPool(conninfo=db_url)


class CategoryQueries:
    def get_all_categories(self, num_results=100, offset=0):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [num_results, offset]
                cur.execute("""
                    SELECT id, title, canon
                    FROM categories
                    ORDER BY id
                    LIMIT %s
                    OFFSET %s
                """, params)

                results = []
                for row in cur.fetchall():
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                    results.append(record)

                return results

    def create_category(self, request):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO categories (title, canon)
                    VALUES (%s, false)
                """, [request.title])

                cur.execute("""
                    SELECT * FROM categories
                    WHERE title = %s
                """, [request.title])

                row = cur.fetchone()
                record = {}
                for i, column in enumerate(cur.description):
                    record[column.name] = row[i]

                return record

    def update_category(self, request, cat_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [request.title, cat_id]
                cur.execute("""
                    UPDATE categories
                    SET title = %s
                    WHERE id = %s
                """, params)

                cur.execute("""
                    SELECT * FROM categories
                    WHERE id = %s
                """, [cat_id])

                row = cur.fetchone()
                record = {}
                for i, column in enumerate(cur.description):
                    record[column.name] = row[i]

                return record

    def delete_category(self, cat_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT * FROM categories
                    WHERE id = %s
                """, [cat_id])

                row = cur.fetchone()

                cur.execute("""
                    DELETE FROM categories
                    WHERE id = %s
                """, [cat_id])

                if row:
                    return True
                else:
                    return False
