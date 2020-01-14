from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/post')
def post():
    pass