# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from app import app
from app.forms import LoginForm, CreateAccountForm

from sql import sql
from sql.sql import ValidateLogin, CreateAccount


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
        results = ValidateLogin(form)
        if results is None or len(results) == 0:
            flash("invalid emil or password")
        else:
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
   form = CreateAccountForm()
   if form.validate_on_submit():
      if CreateAccount(form):
         return redirect(url_for('home'))
      else IntegrityError:
         message = 'Email already exists. Please choose a different email.'
         return render_template('createAccount.html', form=form, message=message)
   return render_template('createAccount.html', form=form)


@app.route('/team/pitching')
def pitching():
   return render_template('pitching.html')


@app.route('/team/batting')
def batting():
   return render_template('batting.html')
