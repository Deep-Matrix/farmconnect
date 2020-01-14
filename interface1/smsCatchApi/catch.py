from flask import Flask, jsonify, request
import os
import sqlite3
app = Flask(__name__)

def getFarmerFromPhone(conn, phno):
    #(No Need to connect again and again. just pass values) conn = sqlite3.connect("././datahouse.db")
    cursor = conn.execute("SELECT FARMERID FROM farmer WHERE PHONENUMBER = " + str(phno))
    row = cursor.fetchone()
    return row[0]

#Assumed Format of SMS
# LINE1: <producename>
# LINE2: <quantityInQuintals>
# LINE3: <costperquintal>
# LINE4: <Description(if any)>

def postdetails(phno, details):
    try:
        path = os.path.realpath('datahouse.db')
        print(path)
        conn = sqlite3.connect(path)
        farmerid = getFarmerFromPhone(conn, phno)
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
            entities = (farmerid, quantityInQuintals, availableQty, sold, description, QualityReviewRating, TimesBought, cost, producename)
            cursor_obj = conn.cursor()
            cursor_obj.execute("INSERT INTO FARMER_PRODUCE(FARMERUSERID, QUANTITY, AVAILABLEQUANTITY, SOLD, DESCRIPTION, QUALITY_REVIEW, NO_TIMES_BOUGHT, COST, PRODUCENAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
            conn.commit()
        else:
            return
    except:
        return

@app.route('/post')
def post():
    phno = request.args.get("phno")
    details = request.args.get("msg")
    print("From: {} \n\n Message: {}".format(phno, details))
    postdetails(phno, details)
    return (jsonify({"status": "ok"}))


if __name__ == '__main__':
    app.run(debug = True)
# postdetails(2121, "wqwqwq")