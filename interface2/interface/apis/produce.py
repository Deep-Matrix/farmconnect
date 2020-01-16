import sqlite3
import os

def totalToStream(conn):
    return conn.execute("SELECT count(*) FROM FARMER_PRODUCE WHERE SOLD = 'False'").fetchone()[0]

def stream(conn):
    conn.row_factory = sqlite3.Row
    data = dict()
    query = "SELECT * FROM FARMER_PRODUCE WHERE SOLD = 'False'"
    # conn = sqlite3.connect(os.path.realpath('datahouse.db'))
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    return rows