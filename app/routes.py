# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')
@app.route('/login')
def login():
   return render_template('login.html')
