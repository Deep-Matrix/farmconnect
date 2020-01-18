from flask import render_template, redirect, jsonify
from app import app
from app.forms import LoginForm
import requests

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("###############################")
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
@app.route('/index')
def index():
    length = 0
    try:
        data = requests.get('http://127.0.0.1:5000/streamproduce').json()
        length = int(requests.get('http://127.0.0.1:5000/streamproducelength').json()['length'])
    except Exception as e:
        print(e)
    arrayt = []
    for i in range(length):
        arrayt.append(data[str(i)])
    
    return render_template('index.html', title='Home Page', produce=arrayt)

@app.route('/produce/<id>')
def produceinformation(id):
    data = {}
    user = {}
    try:
        data = requests.get("http://127.0.0.1:5000/getproduce?id="+str(id)).json()
    except Exception as e:
        print(e)
    return render_template('produce.html', title=str(id)+" - Details", product=data, user=None)
        