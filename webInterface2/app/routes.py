from flask import render_template, redirect
from app import app
from app.forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("###############################")
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)