from flask import Flask, request, jsonify, make_response
from datetime import date
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps



app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        data = request.get_json()
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            conn = connect()
            cursorObj = conn.cursor()
            entities = ((data['farmerid']))
            cursorObj.execute("SELECT * FROM FARMER WHERE FARMERID ==? LIMIT 1;",entities)
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = cursorObj.fetchone()[0]
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login_warehouse_owner')
def login_warehouse_owner():

    auth = request.authorization
    data = request.get_json()
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    #user = User.query.filter_by(name=auth.username).first()
    conn = sqlite3.connect("../interface2/datahouse.db")
    cursorObj = conn.cursor()
    entities = ((data['phone_no']),)
    cursorObj.execute("SELECT * FROM FARMER WHERE PHONENUMBER ==?;",entities)
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = cursorObj.fetchone()

    if current_user == 'null':
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # data = jwt.decode(token, app.config['SECRET_KEY'])
    userpassword = current_user[3]
    xx={}
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
        xx['error'] = str(e)
        return jsonify(xx)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})




@app.route('/register_owner', methods=['POST'])
def register_owner():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['warehouse_id'],data['phone_no'],hashed_password,data['aadhar'],data['photo_url'],data['name']))
        cursorObj.execute("INSERT INTO WAREHOUSE_OWNERS(ID,WAREHOUSE_ID,PHONE_NUMBER,PASSWORD,AADHAR,PHOTO_URL,NAME) VALUES(?,?,?,?,?,?,?)",entities)
        conn.commit()
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New user created!'})

@app.route('/search_warehouse',methods=['POST'])
def search_warehouse():
    pass

@app.route('/list_warehouse',methods=['POST'])
def list_warehouse():
    pass

@app.route('/add_warehouse',methods=['POST'])
def add_warehouse():
    pass

@app.route('/rent_warehouse',methods=['POST'])
def rent_warehouse():
    try:
        data = request.get_json()
        warehouse_id = data['warehouse_id']
        farmer_id = data['farmer_id']
        produce_id = data['produce_id']
        produce_quantity = data['produce_quantity']
        date = data['date']
        time = data['time'] 
        conn = sqlite3.connect('../interface2/datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),warehouse_id,farmer_id,produce_id,produce_quantity,date,time))
        cursorObj.execute("INSERT INTO WAREHOUSE_TRANSACTION(ID,WAREHOUSE_ID,FARMER_ID,PRODUCE_ID,PRODUCE_QUANTITY,DATE,TIME) VALUES(?,?,?,?,?,?);",entities)
        conn.commit()
        cursorObj.execute("SELECT * FROM WAREHOUSE WHERE ID ==?;",(warehouse_id,))
        
    except Exception as e:


# @app.route('/',methods=['POST'])
# def register_warehouse():
#     pass