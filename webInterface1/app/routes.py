from flask import render_template, redirect, jsonify, session
from app import app
from app.forms import LoginForm, SignUpForm, AddProduceForm, CostUpdateForm
import requests
import json


def getSession():
    data = {}
    if isLoggedIn:
        data['address'] = session['address']
        data['datejoined'] = session['datejoined']
        data['fullname'] = session['fullname']
        data['imagelink'] = session['imagelink']
        data['aadhar'] = session['aadhar']
        data['phonenumber'] = session['phonenumber']
        data['userid'] = session['userid']
    return data


def isLoggedIn():
    loggedIn = False
    try:
        data = session['token']
        headers = {'token': data}
        r = requests.post("http://127.0.0.1:5000/farmer_details",headers=headers).json()
        print(r)
        session['address'] = r['address']
        session['datejoined'] = r['datejoined']
        session['fullname'] = r['fullname']
        session['imagelink'] = r['imagelink']
        session['aadhar'] = r['aadhar']
        session['phonenumber'] = r['phonenumber']
        session['userid'] = r['userid']
        loggedIn = True    
    except Exception as e:
        loggedIn = False
        print(str(e))
    return loggedIn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not isLoggedIn():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            r = requests.post('http://127.0.0.1:5000/login_farmer', auth = (username, password))
            print("#########################################" + r.text)
            if r.text == "Could not verify":
                return redirect('/login')
            else:
                print(r.text)
                data = json.loads(r.text)
                session['token'] = data['token']
                print(session['token'])
            return redirect('/farmer_history')
        return render_template('login.html', title='Sign In', form=form, error='Invalid Credentials')
    else:
        return redirect('/')

# @app.route('/')
# @app.route('/index')
# def index():
#     if isLoggedIn():
#         length = 0
#         try:
#             data = requests.get('http://127.0.0.1:7000/streamproduce').json()
#             length = int(requests.get('http://127.0.0.1:7000/streamproducelength').json()['length'])
#         except Exception as e:
#             print(e)
#         arrayt = []
#         for i in range(length):
#             arrayt.append(data[str(i)])
        
#         return render_template('index.html', title='Home Page', produce=arrayt)
    # return redirect('/login')

@app.route('/')
@app.route('/farmer_history')
def index():
    if isLoggedIn():
        try:
            data = requests.post('http://127.0.0.1:5000/farmer_history').json()
        except Exception as e:
            print(e)
        print(data)
        arrayt = []
        for i in data:
            arrayt.append(data[i])
        print(arrayt)
        return render_template('index.html', title='Home Page', transactions=arrayt)
    return redirect('/login')
        
@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password = form.password.data
        address = form.address.data
        phonenum = form.phonenum.data
        fullname = form.address.data
        aadhar = form.aadhar.data
        url = "http://127.0.0.1:5000/registerfarmer"
        payload = {}
        payload['fullname'] = fullname
        payload['password'] = password
        payload['address'] = address
        payload['aadhar'] = aadhar
        payload['phone_no'] = phonenum
        payload['imagelink'] = "some.url.com"
        response = requests.post(url, json = payload).json()
        print(response['error'])
        if response['status'] == "OK":
            return redirect('/login')
        else:
            return render_template('signup.html', form=form, title='Join US', error=response['error'])
    return render_template('signup.html', form=form, title='Join US')

@app.route('/add_produce', methods = ['GET','POST'])
def add_produce():
    # if isLoggedIn:
    #     return redirect('/')
    form = AddProduceForm()
    if form.validate_on_submit():
        producename = form.producename.data
        quantity = form.quantity.data
        cost = form.cost.data
        sold = form.sold.data
        description = form.description.data
        url = "http://127.0.0.1:5000/sell_produce"
        payload = {}
        payload['producename'] = producename
        payload['quantity'] = quantity
        payload['cost'] = cost
        payload['sold'] = False
        payload['quality_review'] = 3
        payload['no_times_bought'] = 0
        payload['description'] = description
        response = requests.post(url, json = payload).json()
        print(response['error'])
        if response['status'] == "OK":
            return redirect('/index')
        else:
            return render_template('addproduce.html', form=form, title='Join US', error=response['error'])
    return render_template('addproduce.html', form=form, title='Join US')

@app.route('/cost_update', methods = ['GET','POST'])
def cost_update():
    # if isLoggedIn:
    #     return redirect('/')
    form = CostUpdateForm()
    if form.validate_on_submit():
        cost = form.cost.data
        url = "http://127.0.0.1:5000/cost_updation"
        payload = {}
        payload['cost'] = cost
        response = requests.post(url, json = payload).json()
        print(response['error'])
        if response['status'] == "OK":
            return redirect('/index')
        else:
            return render_template('cost_update.html', form=form, title='Join US', error=response['error'])
    return render_template('cost_update.html', form=form, title='Join US')

@app.route('/logout')
def logout():
    if isLoggedIn():
        session.clear()
    return redirect('/')