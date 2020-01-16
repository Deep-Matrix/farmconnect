def totalToStream(conn):
    return conn.execute("SELECT count(*) FROM FARMER_PRODUCE WHERE SOLD = 'False'").fetchone()[0]

def stream(conn):
    data = dict()
    query = "SELECT * FROM FARMER_PRODUCE WHERE SOLD = 'False'"
    # conn = sqlite3.connect(os.path.realpath('datahouse.db'))
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    return rows