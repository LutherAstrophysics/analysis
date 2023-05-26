import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
_DB_HOST = os.getenv("DB_HOST") or "localhost"
_DB_PORT = os.getenv("DB_PORT") or 5433


def connect(on_success):
    """
    Connect to our stars data internal database

    param on_success: unary function to be called if the connection is
    successful with the cursor object
    return: the result of calling on_success
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="reader",
        password="mysecretpassword",
        port=_DB_PORT,
        host=_DB_HOST,
    )
    with conn.cursor() as curs:
        try:
            # Go to the appropriate search_path
            curs.execute("SET search_path TO api;")
            return on_success(curs)
        except Exception as e:
            print("connection can't be established")
            raise e


def query(msg):
    """
    Run one line query to the database.
    Raises exception if the query isn't successful

    param msg: The query string
    return: The result of the query
    """

    def inner(cursor):
        cursor.execute(msg)
        return cursor.fetchall()

    return connect(inner)
