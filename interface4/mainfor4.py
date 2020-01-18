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
            entities = ((data['warehouse_owner_id']))
            cursorObj.execute("SELECT * FROM WAREHOUSE_OWNER WHERE WAREHOUSE_OWNER_ID ==? LIMIT 1;",entities)
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
    cursorObj.execute("SELECT * FROM WAREHOUSE_OWNER WHERE PHONENUMBER ==?;",entities)
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = cursorObj.fetchone()

    if current_user == 'null':
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # data = jwt.decode(token, app.config['SECRET_KEY'])
    userpassword = current_user[2]
    xx={}
    #xx['1']=userpassword
    #xx['2']=current_user

    try:
        if check_password_hash(userpassword, auth.password):
            entities = ((data['phone_no']),)
            cursorObj.execute("SELECT WAREHOUSE_OWNER_ID FROM WAREHOUSE_OWNER WHERE PHONENUMBER ==?;",entities)
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            warehouse_owner_id = cursorObj.fetchone() 
            token = jwt.encode({'warehouse_owner_id' : warehouse_owner_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token' : token.decode('UTF-8')})
    except Exception as e:
        xx['msg']='400'
        xx['error'] = str(e)
        return jsonify(xx)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})




#tested - ok
@app.route('/register_owner', methods=['POST'])
def register_owner():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['fullname'],hashed_password,data['address'],data['aadhar'],data['imagelink'],date.today(),data['phone_no']))
        cursorObj.execute("INSERT INTO WAREHOUSE_OWNER(WAREHOUSE_OWNER_ID,FULLNAME,PASSWORD,ADDRESS,AADHAR,IMAGELINK,DATEJOINED,PHONENUMBER) VALUES(?,?,?,?,?,?,?,?);",entities)
        conn.commit()
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New user created!'})

#tested - ok
@app.route('/add_warehouse',methods=['POST'])
def add_warehouse():
    try:
        data = request.get_json()
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        u_id = str(uuid.uuid4())
        entities = ((u_id,data['owner_id'],data['available_size'],data['photo_url'],data['location'],data['cost']))
        cursorObj.execute("INSERT INTO WAREHOUSE(WAREHOUSE_ID,OWNER_ID,AVAILABLE_SIZE,PHOTO_URL,LOCATION,COST) VALUES(?,?,?,?,?,?);",entities)
        conn.commit()
        address_ent = ((u_id,data['latitude'],data['longitude']))
        cursorObj.execute("INSERT INTO WAREHOUSE(WAREHOUSE_ID,OWNER_ID,AVAILABLE_SIZE,PHOTO_URL,LOCATION,COST) VALUES(?,?,?,?,?,?);",entities)
        conn.commit()
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New Warehouse Added!'})

#tested - ok
@app.route('/list_warehouse',methods=['POST'])
def list_warehouse():
    try:
        data = {}
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM WAREHOUSE;")
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['warehouses'] = li
        conn.commit()
    except Exception as e:
        return jsonify({"alert" : "Error!"})    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True,port = 6000)


# @app.route('/',methods=['POST'])
# def register_warehouse():
#     pass
