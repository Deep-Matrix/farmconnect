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

#tested - ok
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
#tested - ok
@app.route('/sell_produce',methods=['POST'])
def sell_produce():
    try:
        data = request.get_json()
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['farmeruserid'],data['quantity'],data['availablequantity'],data['cost'],data['sold'],data['description'],data['quality_review'],data['no_times_bought']))
        cursorObj.execute("INSERT INTO FARMER_PRODUCE(PRODUCEID,FARMERUSERID,QUANTITY,AVAILABLEQUANTITY,COST,SOLD,DESCRIPTION,QUALITY_REVIEW,NO_TIMES_BOUGHT) VALUES (?,?,?,?,?,?,?,?,?);",entities)
        conn.commit()
        #return jsonify({'message' : 'Produce Added!'})
    except Exception as e:
        return jsonify({"alert" : "error!"})
    return jsonify({'message' : 'Produce Added!'})



@app.route('/buy_produce',methods=['POST'])
def buy_produce():
    try:
        data={}
        #data = request.get_json()
        conn = sqlite3.connect("../datahouse.db")
        cursorObj = conn.cursor()
        #entities = ((data['farmeruserid']),)
        #cursorObj.execute("SELECT * FROM FARMER_PRODUCE WHERE PRODUCEID ==?;",entities)
        #current_user = cursorObj.fetchone()

        cursorObj.execute("SELECT * FROM FARMER_PRODUCE;")
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)

        data['produces_bought'] = li
        conn.commit()
    except Exception as e:
        return jsonify({"alert" : "Error!"})    
    return jsonify(data)
        

        #if current_user == 'null':
        #return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        #new_quantity = current_user
    ###except Exception as e:
    ###    print(e)
    #return jsonify({'mess' : current_user},)
    ###return jsonify(data)

#rugved
@app.route('/list_produce',methods=['POST'])
def list_produce():
    pass

#tested - ok
@app.route('/displayfarmers',methods=['POST'])
def displayfarmer():
    try:
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM FARMER;")
        vals = cursorObj.fetchall()
        data = {}
        list_of_farmers =[]
        for val in vals:
            list_of_farmers.append(val)
        data['farmers'] = list_of_farmers
        conn.commit()
    except Exception as e:
        return {"status":"Fail", "message":str(e)}
    return jsonify(data)

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
        # cursorObj.execute("SELECT * FROM WAREHOUSE_OWNER;")
        # vals = cursorObj.fetchone()[0]
        # data['val'] = vals
    except Exception as e:
        data['error'] = str(e)
        return data
    return jsonify({'message' : 'New user created!'})
    # return data

#tested - ok
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

# tested - ok
@app.route('/rent_warehouse',methods=['POST'])
def rent_warehouse():
    try:
        data = request.get_json()
        warehouse_id = data['warehouse_id']
        farmer_id = data['farmer_id']
        produce_id = data['produce_id']
        produce_quantity = data['produce_quantity']
        date = "18/01/20"
        time = "23:23:12"
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),warehouse_id,farmer_id,produce_id,produce_quantity,date,time))
        cursorObj.execute("INSERT INTO WAREHOUSE_TRANSACTION(TRANSACTION_ID,WAREHOUSE_ID,FARMER_ID,PRODUCE_ID,PRODUCE_QUANTITY,DATE,TIME) VALUES(?,?,?,?,?,?,?);",entities)
        conn.commit()
        cursorObj.execute("SELECT * FROM WAREHOUSE WHERE WAREHOUSE_ID ==?;",(warehouse_id,))
        row = cursorObj.fetchone()[2]
        new_data = row
        ware_id = warehouse_id
        new_quantity = new_data - int(produce_quantity)
        entities=((new_quantity,ware_id))
        cursorObj.execute("UPDATE WAREHOUSE SET AVAILABLE_SIZE = ? WHERE WAREHOUSE_ID == ?",entities)
        # return jsonify({"message": new_quantity})
        conn.commit() 
    except Exception as e:
        return jsonify({'message':str(e)})
    return jsonify({"message":"Warehouse has been rented"})

if __name__ == '__main__':
    app.run(debug=True)
