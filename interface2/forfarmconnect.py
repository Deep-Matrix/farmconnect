from flask import Flask, request, jsonify, make_response
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/api_example/todo.db'

# db = SQLAlchemy(app)


@app.route('/farmeruser', methods=['POST'])
##@token_required
def create_user():
#    if not current_user.admin:
#        return jsonify({'message' : 'Cannot perform that function!'})
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # data={}
    conn = sqlite3.connect("datahouse.db")
    cursorObj = conn.cursor()
    entities = ((str(uuid.uuid4()),data['address'],data['fname'],hashed_password,data['aadhar'],data['imagelink'],date.today() ,data['phone_no']))
    cursorObj.execute("INSERT INTO FARMER(FARMERID,ADDRESS,FULLNAME,PASSWORD,AADHAR,IMAGELINK,DATEJOINED,PHONENUMBER) VALUES(?,?,?,?,?,?,?,?)",entities)
    # cursorObj.execute("SELECT * FROM FARMER;")
    # vals = cursorObj.fetchall()
    # li = []
    # for val in vals:
    #     li.append(val)

    # data['listads===_x'] = li
    # data = {"X":vals}
    # print(vals)
    # # for val in vals:
    #     print(val)
    conn.commit()

    return jsonify({'message' : 'New user created!'})
    # return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
