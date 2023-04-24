# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

import pymysql
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash

from app import app
from app.forms import LoginForm, CreateAccountForm

con = pymysql.connect(host='localhost', user='root', password='Cars0n200!', db='littleleauge')
cur = con.cursor()


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
        sql = "SELECT * FROM user WHERE email = %s AND password = %s"
        passwordHash = generate_password_hash(form.password.data)

        params = [form.email.data, passwordHash]
        cur.execute(sql, params)
        results = cur.fetchall()
        if results is None or len(results) == 0:
            flash("invalid emil or password")
        else:
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        sql = "INSERT INTO user (email, name, password) VALUES (%s, %s, %s)"
        passwordHash = generate_password_hash(form.password.data)
        name = form.nameF.data + " " + form.nameL.data

        params = [form.email.data, name, passwordHash]

        try:
            cur.execute(sql, params)
            con.commit()
            con.close()
            return redirect(url_for('home'))
        except IntegrityError:
            message = 'Email already exists. Please choose a different email.'
            return render_template('createAccount.html', form=form, message=message)
    return render_template('createAccount.html', form=form)
