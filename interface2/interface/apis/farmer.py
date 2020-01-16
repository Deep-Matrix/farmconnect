def getNameFromId(conn, id):
    #(No Need to connect again and again. just pass values) conn = sqlite3.connect("././datahouse.db")
    cursor = conn.execute("SELECT FULLNAME FROM farmer WHERE FARMERID = " + str(id))
    row = cursor.fetchone()
    return row[0]