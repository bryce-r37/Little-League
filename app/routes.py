# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/home')
def home():
   return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
      flash('Login requested for email {}'.format(
               form.email.data))
      return redirect(url_for('home'))
   return render_template('login.html', form=form)

@app.route('/createAccount')
def createAccount():
   return render_template('createAccount.html')
