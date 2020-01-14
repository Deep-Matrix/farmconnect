from datetime import datetime
from flask import Flask
import requests

app = Flask(__name__)


# @app.route('/sell_produce',methods=['POST'])
# def sell_produce():
#     pass


@app.route('/buy_produce',methods=['POST'])
def buy_produce():
    pass


@app.route('/list_produce',methods=['POST'])
def list_produce():
    pass


@app.route('/put_review',methods=['POST'])
def put_review():
    pass


@app.route('/list_review',methods=['POST'])
def list_reviews():
    pass


@app.route('/farmer_history',methods=['POST'])
def farmer_history():
    pass



@app.route('/buyer_history',methods=['POST'])
def buyer_history():
    pass


# @app.route('/search_produce',methods=['POST'])
# def search():  #from list produce
#     pass


@app.route('/category_sort',methods=['POST'])
def category_sort():
    pass


@app.route('/price_sort',methods=['POST'])
def price_sort():
    pass

@app.route('/review_sort',methods=['POST'])
def review_sort():
    pass











