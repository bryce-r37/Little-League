# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/login')
def login():
   form = LoginForm()
   return render_template('login.html', title='Sign In', form=form)
