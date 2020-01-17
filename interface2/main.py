from flask import Flask, request, jsonify, make_response
from datetime import date
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from interface import stream_produce, create_farmer

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/api_example/todo.db'

# db = SQLAlchemy(app)

def connect():
    # Sharing same reference across project to save memory and also, it makes updating database path easier.
    conn = sqlite3.connect("datahouse.db")
    conn.row_factory = sqlite3.Row
    return conn

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

# This interface will create farmer's entry in database
# input:
# {
#     "address":""
#     "fname":""
#     "password":""
#     "aadhar":""
#     "imagelink":""
#     "phone_no"
# }
# returns:
# {
#     "status":"OK/Fail"
#     "message":"New User Created./Error Message"
# }

@app.route('/registerfarmer', methods=['GET', 'POST'])
def create_user():
    try:
        data = request.get_json()
        data['password'] = generate_password_hash(data['password'], method='sha256')
        conn = connect()
        return jsonify(create_farmer.create(conn, data))
    except:
        return jsonify({"message":"post required", "status":"fail"})

@app.route('/login')
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
    xx={}
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
    data={}
    try:
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM QUALITY_REVIEW;")
        vals = cursorObj.fetchall()
        list_of_reviews =[]
        for val in vals:
            list_of_reviews.append(val)
        data['reviews'] = list_of_reviews
    except Exception as e:
        data['errors'] = str(e)
    return jsonify(data)

#talha
@app.route('/farmer_history')
def farmer_history():
    try:
        conn = connect
        cursorObj = conn.cursor()
        data = request.get_json()
        entities=((data['farmerid']))
        cursorObj.execute("SELECT ID FROM BUSINESS_HISTORY WHERE PRODUCE_ID=(SELECT PRODUCE_ID FROM FARMER_PRODUCE WHERE FARMER_ID ==?)",entities)
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['list'] = li
    except Exception as e:
        data['errors'] = str(e)
    return jsonify(data)


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

# This api will be used to display available produce.
# return:
# {
#     "0":{
#         "produceid": ""
#         "producename": ""
#         "farmername": ""
#         "availableqty": "" (in quintals)
#         "cost": "" (per quintal)
#         "description": ""
#         "qualityreview": ""
#         "notimebought": ""
#     }
#     "1":{
#         same
#     }
#     so on (till length)
# } 
@app.route('/streamproduce')
def streamproduce():
    conn = connect()
    return (jsonify(stream_produce.get(conn)))


# This function returns length of producestream. It can be used to run loops
# Return Format:
# {
#     "length":""
# }
@app.route('/streamproducelength')
def streamlength():
    conn = connect()
    return jsonify(stream_produce.length(conn))

# This api returns details of specific produce.
# It will be used to build specific page for product.
# return:
# {
#         "produceid": ""
#         "producename": ""
#         "farmername": ""
#         "availableqty": "" (in quintals)
#         "cost": "" (per quintal)
#         "description": ""
#         "qualityreview": ""
#         "notimebought": ""
#     }
@app.route('/getproduce')
def getproduce():
    reqid = request.args.get('id')
    conn = connect()
    return jsonify(stream_produce.item(conn, reqid))

#"228cfd8c-209c-4117-9e6f-0130571053b8" --> user id
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
        cursorObj.execute("SELECT * FROM WAREHOUSE_OWNER;")
        vals = cursorObj.fetchone()[0]
        data['val'] = vals
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New user created!'})
    # return data

@app.route('/add_warehouse',methods=['POST'])
def add_warehouse():
    try:
        data = request.get_json()
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['owner_id'],data['available_size'],data['photo_url'],data['location'],data['cost']))
        cursorObj.execute("INSERT INTO WAREHOUSE(WAREHOUSE_ID,OWNER_ID,AVAILABLE_SIZE,PHOTO_URL,LOCATION,COST) VALUES(?,?,?,?,?,?);",entities)
        conn.commit()
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New Warehouse Added!'})

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
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),warehouse_id,farmer_id,produce_id,produce_quantity,date,time))
        cursorObj.execute("INSERT INTO WAREHOUSE_TRANSACTION(ID,WAREHOUSE_ID,FARMER_ID,PRODUCE_ID,PRODUCE_QUANTITY,DATE,TIME) VALUES(?,?,?,?,?,?);",entities)
        conn.commit()
        cursorObj.execute("SELECT * FROM WAREHOUSE WHERE WAREHOUSE_ID ==?;",(warehouse_id,))
        conn.commit()
        row = cursorObj.fetchone()[0]
        id_x = row[0]
        new_data = row[2]-produce_quantity
        entities=((new_data,id_x))
        cursorObj.execute("UPDATE WAREHOUSE SET AVAILABLE_SIZE = ? WHERE WAREHOUSE_ID == ?",entities) 
        conn.commit()
    except Exception as e:
        return jsonify({'message':"Error"})
    return jsonify({"message":"Warehouse has been rented"})

@app.route('/list_owner_warehouse',methods=['POST'])
def list_owner_warehouses():
    try:
        data={}
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        data = request.get_json()
        owner_id = data['owner_id']
        cursorObj.execute("SELECT * FROM WAREHOUSE WHERE OWNER_ID ==?;",(owner_id,))
        rows = cursorObj.fetchall()
        li=[]
        for row in rows:
            li.append(row)
        data['warehouses'] = li
    except Exception as e:
        data['error'] = str(e)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
