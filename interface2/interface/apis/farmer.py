from datetime import date
import uuid

def getNameFromId(conn, id):
    #(No Need to connect again and again. just pass values) conn = sqlite3.connect("././datahouse.db")
    cursor = conn.execute("SELECT FULLNAME FROM farmer WHERE FARMERID = " + str(id))
    row = cursor.fetchone()
    return row[0]

def createFarmerUser(conn, data):
    try:
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['address'],data['fname'],data['password'],data['aadhar'],data['imagelink'],date.today() ,data['phone_no']))
        cursorObj.execute("INSERT INTO FARMER(FARMERID,ADDRESS,FULLNAME,PASSWORD,AADHAR,IMAGELINK,DATEJOINED,PHONENUMBER) VALUES(?,?,?,?,?,?,?,?)",entities)
        conn.commit()
        return {"status":"OK", "message":"New User Created."}
    except Exception as e:
        return {"status":"Fail", "message":str(e)}