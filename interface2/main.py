from flask import Flask, request, jsonify, make_response
import datetime
import sqlite3
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from math import sin, cos, sqrt, atan2
import os
from interface import stream_produce, create_farmer

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/api_example/todo.db'
# db = SQLAlchemy(app)

def connect():
    # Sharing same reference across project to save memory and also, it makes updating database path easier.
    conn = sqlite3.connect(os.path.realpath("datahouse.db"))
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
    except Exception as e:
        print(e)
        return jsonify({"message":"post required", "status":"fail","error":str(e)})

@app.route('/registerbuyer', methods=['POST'])
def registerbuyer():
    data={}
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),data['fullname'],hashed_password,data['address'],data['aadhar'],data['imagelink'],datetime.datetime.utcnow(),data['phone_no']))
        cursorObj.execute("INSERT INTO BUYER(BUYERID,FULLNAME,PASSWORD,ADDRESS,AADHAR,IMAGELINK,DATEJOINED,PHONENUMBER) VALUES(?,?,?,?,?,?,?,?);",entities)
        conn.commit()
    except Exception as e:
        data['error'] = str(e)
        return jsonify({"alert" : str(e), 'status':'FAIL'})
    return jsonify({'message' : 'New Buyer created!', 'status':'OK'})

#Tested ok. Website Done!!
@app.route('/login_farmer',methods=['POST'])
def login_farmer():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


    #user = User.query.filter_by(name=auth.username).first()
    conn = connect()
    cursorObj = conn.cursor()
    entities = ((auth.username),)
    cursorObj.execute("SELECT * FROM FARMER WHERE PHONENUMBER ==?;",entities)
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = cursorObj.fetchone()
    if not current_user:
        return jsonify({"status":"FAIL"})

    if current_user == 'null':
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # data = jwt.decode(token, app.config['SECRET_KEY'])
    userpassword = current_user[3]
    xx={}
    try:
        if check_password_hash(userpassword, auth.password):
            entities = ((auth.username),)
            cursorObj.execute("SELECT FARMERID FROM FARMER WHERE PHONENUMBER ==?;",entities)
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            farmerid = cursorObj.fetchone()[0]
            token = jwt.encode({'farmerid' : farmerid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token' : token.decode('UTF-8')})
    except Exception as e:
        xx['msg']='400'
        xx['error'] = str(e)
        return jsonify(xx)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/login_buyer',methods=['POST'])
def login_buyer():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    #user = User.query.filter_by(name=auth.username).first()
    conn = connect()
    cursorObj = conn.cursor()
    entities = (auth.username,)
    cursorObj.execute("SELECT * FROM BUYER WHERE PHONENUMBER ==?;",entities)
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = cursorObj.fetchone()
    if not current_user:
        return jsonify({"status":"FAIL"})

    if current_user == 'null':
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # data = jwt.decode(token, app.config['SECRET_KEY'])
    userpassword = current_user[2]
    xx={}
    try:
        if check_password_hash(userpassword, auth.password):
            entities = (auth.username,)
            cursorObj.execute("SELECT BUYERID FROM BUYER WHERE PHONENUMBER ==?;",entities)
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            buyerid = cursorObj.fetchone()[0] 
            token = jwt.encode({'buyerid' : buyerid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token' : token.decode('UTF-8')})
    except Exception as e:
        xx['msg']='400'
        xx['error'] = str(e)
        return jsonify(xx)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/buyer_details',methods=['POST']) 
def buyer_details():
    try:
        conn = connect()
        cursorObj = conn.cursor()
        token = request.headers.get('token')
        dict_token = jwt.decode(token,app.config['SECRET_KEY'])
        value = dict_token['buyerid']
        cursorObj.execute("SELECT * FROM BUYER WHERE BUYERID ==?;",(value,))
        user_data = cursorObj.fetchone()
        new_dict={}
        new_dict['userid'] = user_data['BUYERID']
        new_dict['fullname'] = user_data['FULLNAME']
        new_dict['address'] = user_data['ADDRESS']
        new_dict['imagelink'] = user_data['IMAGELINK']
        new_dict['datejoined'] = user_data['DATEJOINED']
        new_dict['phonenumber'] = user_data['PHONENUMBER']
        new_dict['status'] = 'OK'
    except Exception as e:
        new_dict={}
        new_dict['status']="FAIL"
        new_dict['error']=str(e) 
    return jsonify(new_dict)


#tested - ok
@app.route('/sell_produce',methods=['POST'])
def sell_produce():
    try:
        data = request.get_json()
        conn = connect()
        cursorObj = conn.cursor()
        token = request.headers.get('token')
        dict_token = jwt.decode(token,app.config['SECRET_KEY'])
        value = dict_token['farmerid']
        entities = ((str(uuid.uuid4()),value,data['quantity'],data['availablequantity'],data['cost'],data['sold'],data['description'],data['quality_review'],data['no_times_bought']))
        cursorObj.execute("INSERT INTO FARMER_PRODUCE(PRODUCEID,FARMERUSERID,QUANTITY,AVAILABLEQUANTITY,COST,SOLD,DESCRIPTION,QUALITY_REVIEW,NO_TIMES_BOUGHT) VALUES (?,?,?,?,?,?,?,?,?);",entities)
        conn.commit()
        #return jsonify({'message' : 'Produce Added!'})
    except Exception as e:
        return jsonify({"alert" : str(e)})
    return jsonify({'message' : 'Produce Added!'})


#tested - ok #website ok
@app.route('/buy_produce',methods=['POST'])
def buy_produce():
    try:
        data = request.get_json()
        conn = connect()
        cursorObj = conn.cursor()
        token = request.headers.get('token')
        dict_token = jwt.decode(token,app.config['SECRET_KEY'])
        value = dict_token['buyerid']
        date_string = datetime.datetime.now().strftime("%m/%d/%Y")
        time_string = datetime.datetime.now().strftime("%H:%M:%S")
        entities = ((str(uuid.uuid4()),value,data['produce_id'],data['quantity'],date_string,time_string))
        cursorObj.execute("SELECT * FROM FARMER_PRODUCE WHERE PRODUCEID == ?;",(data['produce_id'],))
        tup = cursorObj.fetchone()  #previous quantity of produce
        previous_quantity = tup[3]
        previous_times_bought = tup[8]
        bought_quantity = int(data['quantity'])
        final = previous_quantity - bought_quantity
        if final < 0:
            return jsonify({"STATUS" : "FAIL","message":"Not Enough Quantity"})
        entities = ((final,data['produce_id']))
        cursorObj.execute("UPDATE FARMER_PRODUCE SET AVAILABLEQUANTITY = ? WHERE PRODUCEID == ?",entities)
        updated_times_bought = 1 + previous_times_bought
        entities = ((updated_times_bought,data['produce_id']))
        cursorObj.execute("UPDATE FARMER_PRODUCE SET NO_TIMES_BOUGHT = ? WHERE PRODUCEID == ?",entities)
        if final == 0:
            value_boolean = True
            entities = ((value_boolean,data['produce_id']))
            cursorObj.execute("UPDATE FARMER_PRODUCE SET SOLD = ? WHERE PRODUCEID == ?",entities) 
        cursorObj.execute("INSERT INTO BUSINESS_HISTORY(ID,BUYERID,PRODUCEID,QUANTITY,DATE,TIME) VALUES (?,?,?,?,?,?);",entities)
        conn.commit()
    except Exception as e:
        return jsonify({"STATUS" : "FAIL","message":str(e)})
    return jsonify({"STATUS" : "OK","message":"Bought successfully"})    

#tested-ok
@app.route('/list_produce',methods=['POST'])
def list_produce():
    try:
        data={}
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM FARMER_PRODUCE;")
        li = []
        vals = cursorObj.fetchall()
        for val in vals:
            li.append(val)
        data['list'] = li
        data['status'] = "OK"
    except Exception as e:
        data['status'] = "FAIL"
    return jsonify(data)


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

#tested = ok
@app.route('/put_review',methods=['POST'])
def put_review():
    try:
        data = request.get_json()
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        date_string = datetime.now().strftime("%m/%d/%Y")
        time_string = datetime.now().strftime("%H:%M:%S")
        entities = ((str(uuid.uuid4()),data['buyer_id'],data['produce_id'],data['rating'],date_string,time_string))
        cursorObj.execute("INSERT INTO QUALITY_REVIEW(ID,BUYERID,PRODUCEID,RATING,DATE,TIME) VALUES (?,?,?,?,?,?);",entities)
        conn.commit()
        cursorObj.execute("SELECT * FROM QUALITY_REVIEW WHERE PRODUCEID ==?;",(data['produce_id'],))
        vals = cursorObj.fetchall()
        # data_new = {} 
        # list_of_reviews =[]
        sum=0
        count = 0
        for val in vals:
            sum+=val[3]
            count+=1
        avg = sum/count
        entities=((avg,data['produce_id']))
        cursorObj.execute("UPDATE FARMER_PRODUCE SET QUALITY_REVIEW = ? WHERE PRODUCEID == ?",entities)
        conn.commit() 
    except Exception as e:
        return jsonify({'message':str(e)})
    return jsonify({"VALS" : avg, 'message' : 'Review Added!'})


#tested - ok
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

#tested-ok
@app.route('/farmer_history',methods=['POST'])
def farmer_history():
    try:
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        data = request.get_json()
        cursorObj.execute("SELECT ID FROM BUSINESS_HISTORY WHERE PRODUCEID=(SELECT PRODUCEID FROM FARMER_PRODUCE WHERE FARMERUSERID ==?)",(data['farmer_id'],))
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['list'] = li
    except Exception as e:
        data={}
        data['errors'] = str(e)
    return jsonify(data)


@app.route('/cost_updation',methods=['POST'])
def cost_updation():
    data = request.get_json
    conn = sqlite3.connect("datahouse.db")
    cursorObj = conn.cursor()
    entities = ((data['cost'],data['produce_id']))
    cursorObj.execute("UPDATE FARMER_PRODUCE SET COST = ? WHERE PRODUCEID == ?",entities)
    conn.commit()
    return jsonify({"message" : "COST UPDATED"})

#tested-ok
@app.route('/buyer_history',methods=['POST'])
def buyer_history():
    data = {}
    try:
        conn = connect()
        cursorObj = conn.cursor()
        token = request.headers.get('token')
        dict_token = jwt.decode(token,app.config['SECRET_KEY'])
        value = dict_token['buyerid']
        cursorObj.execute("SELECT * FROM BUSINESS_HISTORY WHERE BUYERID == ? ORDER BY DATE;",(value,))
        vals = cursorObj.fetchall()
        li = {}
        li1=[]
        counter = 0
        # for val in vals:
        print(vals[1]['PASSWORD'])
        data['buyer_history'] = li
        data['status'] = "OK"
    except Exception as e:
        data['error'] =  str(e)
        data['status'] = "FAIL"
    return jsonify(data)

# @app.route('/search_produce',methods=['POST'])  TO-BE DONE LATER
# def search():  #from list produce
#     pass


@app.route('/category_sort',methods=['POST'])
def category_sort():
    try:
        data = request.get_json
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        entities = ((data['category']))
        cursorObj.execute("SELECT * FROM FARMER_PRODUCE WHERE TYPE ==? AND SOLD == False;",entities)
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['status'] = "OK"
        data['categorical_products'] = li 
    except Exception as e:
        data['status'] = "FAIL"
    return jsonify(data)

#tested - ok
@app.route('/price_sort',methods=['POST'])
def price_sort():
    try:
        data = {}
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM FARMER_PRODUCE ORDER BY COST;")
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['status'] = "OK"
        data['price_products'] = li 
    except Exception as e:
        data['status'] = "FAIL"
        data['error'] = str(e)
    return jsonify(data)


#tested-ok
@app.route('/review_sort',methods=['POST'])
def review_sort():
    try:
        data = {}
        conn = sqlite3.connect("datahouse.db")
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM FARMER_PRODUCE ORDER BY QUALITY_REVIEW;")
        vals = cursorObj.fetchall()
        li = []
        for val in vals:
            li.append(val)
        data['status'] = "OK"
        data['review_products'] = li 
    except Exception as e:
        data['status'] = "FAIL"
        data['error'] = str(e)
    return jsonify(data)

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


# tested - ok
@app.route('/rent_warehouse',methods=['POST'])
def rent_warehouse():
    try:
        data = request.get_json()
        warehouse_id = data['warehouse_id']
        farmer_id = data['farmer_id']
        produce_id = data['produce_id']
        produce_quantity = data['produce_quantity']
        date_string = datetime.now().strftime("%m/%d/%Y")
        time_string = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        entities = ((str(uuid.uuid4()),warehouse_id,farmer_id,produce_id,produce_quantity,date_string,time_string))
        cursorObj.execute("INSERT INTO WAREHOUSE_TRANSACTION(TRANSACTION_ID,WAREHOUSE_ID,FARMER_ID,PRODUCE_ID,PRODUCE_QUANTITY,DATE,TIME) VALUES(?,?,?,?,?,?,?);",entities)
        conn.commit()
        cursorObj.execute("SELECT * FROM WAREHOUSE WHERE WAREHOUSE_ID ==?;",(warehouse_id,))
        row = cursorObj.fetchone()[2]
        new_data = row
        new_quantity = new_data - int(produce_quantity)
        entities=((new_quantity,warehouse_id))
        cursorObj.execute("UPDATE WAREHOUSE SET AVAILABLE_SIZE = ? WHERE WAREHOUSE_ID == ?",entities)
        # return jsonify({"message": new_quantity})
        conn.commit() 
    except Exception as e:
        return jsonify({'message':str(e)})
    return jsonify({"message":"Warehouse has been rented"})

def calculate_distance(lat1,lon1,lat2,lon2):
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def Sort(sub_li): 
    return(sorted(sub_li, key = lambda x: x[1]))

#-----------------------------------------
@app.route('/search_warehouse',methods=['POST'])
def search_warehouse():
    try:
        data = request.get_json()
        user_loc_lat , user_loc_lon = data['latitude'],data['longitude']   
        conn = sqlite3.connect('datahouse.db')
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM WAREHOUSE_ADDRESS;")
        warehouses = cursorObj.fetchall()
        warehouse_list=[]
        for warehouse in warehouses:
            temp_list = []
            logintemp_list.append(warehouse[0])
            distance = calculate_distance(user_loc_lat , user_loc_lon,warehouse[1],warehouse[2])
            temp_list.append(distance)
            warehouse_list.append(temp_list)
        sorted_list = Sort(warehouse_list)
        optimal_data = {"list":sorted_list}
        optimal_data['status'] = "OK" 
    except Exception as e:
        optimal_data['status'] = "FAIL"
    return jsonify(optimal_data)


@app.route('/farmer_details',methods=['POST']) 
def farmer_details():
    try:
        conn = connect()
        cursorObj = conn.cursor()
        token = request.headers.get('token')
        dict_token = jwt.decode(token,app.config['SECRET_KEY'])
        value = dict_token['buyerid']
        cursorObj.execute("SELECT * FROM FARMER WHERE FARMERID ==?;",(value,))
        user_data = cursorObj.fetchone()
        new_dict={}
        new_dict['userid'] = user_data['FARMERID']
        new_dict['fullname'] = user_data['FULLNAME']
        new_dict['address'] = user_data['ADDRESS']
        new_dict['imagelink'] = user_data['IMAGELINK']
        new_dict['imagelink'] = user_data['AADHAR']
        new_dict['datejoined'] = user_data['DATEJOINED']
        new_dict['phonenumber'] = user_data['PHONENUMBER']
        new_dict['status'] = 'OK'
    except Exception as e:
        new_dict={}
        new_dict['status']="FAIL"
        new_dict['error']=str(e) 
    return jsonify(new_dict)


if __name__ == '__main__':
    app.run(debug=True)
