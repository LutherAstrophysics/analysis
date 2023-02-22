import psycopg2


def connect(on_success):
    """
    Connect to our stars data internal database

    param on_success: unary function to be called if the connection is
    successful with ther cursor object
    return: the result of calling on_success
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="reader",
        password="mysecretpassword",
        port=5433,
        host="localhost",
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
