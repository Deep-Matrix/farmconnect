import sqlite3
import datetime
"""
Name -> identify
Type -> get
Qty -> get
Cost -> get
Farmerid -> iden
sold -> False
QualityReR -> 2.5
TimesBought -> 
Description
"""
def getFarmerFromPhone(phno):
    conn = sqlite3.connect("../../maindata.db")
    cursor = conn.execute("SELECT userid FROM FARMER where PHONENUMBER = " + str(phno))
    rows = cursor.fetchone()
    if row not None:
        return row[0]


def postdetails(phno, details):
    


getFarmerFromPhone(90909)