import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect("voting.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

#  import sqlite3

# def get_connection():
#     conn = sqlite3.connect("voting.db")
#     return conn