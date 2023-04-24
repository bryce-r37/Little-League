# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, CreateAccountForm


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
   form = CreateAccountForm()
   if form.validate_on_submit():
      flash('CreateAccount requested for nameF {}, nameL {}, email {}, password {}'.format(
               form.nameF.data, form.nameL.data, form.email.data,
               form.password.data))
      return redirect(url_for('home'))
   return render_template('createAccount.html', form=form)

@app.route('/team/pitching')
def pitching():
   return render_template('pitching.html')

@app.route('/team/batting')
def batting():
   return render_template('batting.html')
