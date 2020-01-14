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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            conn = sqlite3.connect("datahouse.db")
            cursorObj = conn.cursor()
            entities = ((data['farmerid']))
            cursorObj.execute("SELECT * FROM FARMER WHERE FARMERID ==? LIMIT 1;",entities)
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = cursorObj.fetchone()[0]
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/farmeruser', methods=['POST'])
@token_required
def create_user(current_user):
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

@app.route('/login')
@token_required
def login():

    auth = request.authorization
    data = request.get_json()
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    #user = User.query.filter_by(name=auth.username).first()
    conn = sqlite3.connect("datahouse.db")
    cursorObj = conn.cursor()
    entities = ((data['phone_no']),)
    cursorObj.execute("SELECT * FROM FARMER WHERE PHONENUMBER ==?;",entities)
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = cursorObj.fetchone()

    if current_user == 'null':
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # data = jwt.decode(token, app.config['SECRET_KEY'])
    userpassword = current_user[3]
    #xx={}
    #xx['1']=userpassword
    #xx['2']=current_user

    try:
        if check_password_hash(userpassword, auth.password):
            entities = ((data['phone_no']),)
            cursorObj.execute("SELECT FARMERID FROM FARMER WHERE PHONENUMBER ==?;",entities)
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            farmerid = cursorObj.fetchone() 
            token = jwt.encode({'farmerid' : farmerid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token' : token.decode('UTF-8')})
    except Exception as e:
        xx['msg']='400'
        return jsonify(xx)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


#Tushar
@app.route('/sell_produce',methods=['POST'])
def sell_produce():
    pass

#tushar
@app.route('/buy_produce',methods=['POST'])
def buy_produce():
    pass

#rugved
@app.route('/list_produce',methods=['POST'])
def list_produce():
    pass

#vinit
@app.route('/put_review',methods=['POST'])
def put_review():
    pass

#talha
@app.route('/list_review',methods=['POST'])
def list_reviews():
    pass

#talha
@app.route('/farmer_history',methods=['POST'])
def farmer_history():
    pass


#vinit
@app.route('/buyer_history',methods=['POST'])
def buyer_history():
    pass


# @app.route('/search_produce',methods=['POST'])  TO-BE DONE LATER
# def search():  #from list produce
#     pass

#rugved
@app.route('/category_sort',methods=['POST'])
def category_sort():
    pass


#rugved
@app.route('/price_sort',methods=['POST'])
def price_sort():
    pass


#rugved
@app.route('/review_sort',methods=['POST'])
def review_sort():
    pass



if __name__ == '__main__':
    app.run(debug=True)
