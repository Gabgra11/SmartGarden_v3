import psycopg
import os

with psycopg.connect(os.environ.get('db_url')) as connection:
    with connection.cursor() as cur:
        cur.execute(open("schema.sql", "r").read())
        connection.commit()