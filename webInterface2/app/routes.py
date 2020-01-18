from flask import render_template, redirect, jsonify, session
from app import app
from app.forms import LoginForm, SignUpForm
import requests
import json

def getSession():
    data = {}
    if isLoggedIn:
        data['addres'] = session['address']
        data['datejoined'] = session['datejoined']
        data['fullname'] = session['fullname']
        data['imagelink'] = session['imagelink']
        data['phonenumber'] = session['phonenumber']
        data['userid'] = session['userid']
    return data

def isLoggedIn():
    loggedIn = False
    try:
        data = session['token']
        headers = {'token': data}
        r = requests.post("http://127.0.0.1:5000/buyer_details",headers=headers).json()
        session['address'] = r['address']
        session['datejoined'] = r['datejoined']
        session['fullname'] = r['fullname']
        session['imagelink'] = r['imagelink']
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
            r = requests.post('http://127.0.0.1:5000/login_buyer', auth = (username, password))
            print("#########################################" + r.text)
            if r.text == "Could not verify":
                return redirect('/login')
            else:
                print(r.text)
                data = json.loads(r.text)
                session['token'] = data['token']
                print(session['token'])
            return redirect('/index')
        return render_template('login.html', title='Sign In', form=form, error='Invalid Credentials')
    else:
        return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    if isLoggedIn():
        length = 0
        try:
            data = requests.get('http://127.0.0.1:5000/streamproduce').json()
            length = int(requests.get('http://127.0.0.1:5000/streamproducelength').json()['length'])
        except Exception as e:
            print(e)
        arrayt = []
        for i in range(length):
            arrayt.append(data[str(i)])
        
        return render_template('index.html', title='Home Page', produce=arrayt, user=getSession())
    return redirect('/login')

@app.route('/produce/<id>')
def produceinformation(id):
    data = {}
    user = {}
    try:
        data = requests.get("http://127.0.0.1:5000/getproduce?id="+str(id)).json()
    except Exception as e:
        print(e)
    return render_template('produce.html', title=str(id)+" - Details", product=data, user=session)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    # if isLoggedIn:
    #     return redirect('/')
    form = SignUpForm()
    if form.validate_on_submit():
        password = form.password.data
        address = form.address.data
        phonenum = form.phonenum.data
        fullname = form.address.data
        aadhar = form.aadhar.data
        url = "http://127.0.0.1:5000/registerbuyer"

        payload = {}
        payload['fullname'] = fullname
        payload['password'] = password
        payload['address'] = address
        payload['aadhar'] = aadhar
        payload['phone_no'] = phonenum
        payload['imagelink'] = "some.url.com"
        response = requests.post(url, json = payload).json()

        if response['status'] == "OK":
            return redirect('/login')
        else:
            return render_template('signup.html', form=form, title='Join US', error='Some Error Occurred')
    return render_template('signup.html', form=form, title='Join US')

@app.route('/logout')
def logout():
    if isLoggedIn():
        session.clear()
    return redirect('/')