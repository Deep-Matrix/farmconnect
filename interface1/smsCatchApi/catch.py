from flask import Flask, jsonify, request
import os
import sqlite3
import uuid

app = Flask(__name__)

def getFarmerFromPhone(conn, phno):
    #(No Need to connect again and again. just pass values) conn = sqlite3.connect("././datahouse.db")
    cursor = conn.execute("SELECT FARMERID FROM FARMER WHERE PHONENUMBER = ?" , (str(phno).strip('+91'),))
    row = cursor.fetchone()
    print(row)
    return row[0]

#Assumed Format of SMS
# LINE1: <producename>
# LINE2: <quantityInQuintals>
# LINE3: <costperquintal>
# LINE4: <Description(if any)>

def postdetails(phno, details):
    path = os.path.realpath('/Users/aman/Documents/GitHub/farmconnect/datahouse.db')
    print(path)
    conn = sqlite3.connect(path)
    farmerid = getFarmerFromPhone(conn, phno)
    print(farmerid)
    form = details.splitlines()
    if form:
        producename = form[0]
        quantityInQuintals = form[1]
        cost = form[2]
        availableQty = quantityInQuintals
        if len(form) > 2:
            description = form[3]
        else:
            description = ""
        # produceid = getProduceIdfromName(producename)
        sold = "False"
        QualityReviewRating = "2.5"
        TimesBought = "0"
        entities = (str(uuid.uuid4()), farmerid, quantityInQuintals, availableQty, sold, description, QualityReviewRating, TimesBought, cost, producename)
        cursor_obj = conn.cursor()
        cursor_obj.execute("INSERT INTO FARMER_PRODUCE(PRODUCEID, FARMERUSERID, QUANTITY, AVAILABLEQUANTITY, SOLD, DESCRIPTION, QUALITY_REVIEW, NO_TIMES_BOUGHT, COST, PRODUCENAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
        conn.commit()
    else:
        return

@app.route('/post', methods = ["POST", "GET"])
def post():
    phno = request.form["phone_no"]
    details = request.form["details"]
    print("From: {} \n\n Message: {}".format(phno, details))
    postdetails(phno, details)
    return (jsonify({"status": "ok"}))


if __name__ == '__main__':
    app.run(debug = True, port = 5005)
# postdetails(2121, "wqwqwq")