# file: routes.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

import pymysql
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
        sql = "SELECT password FROM user WHERE email = %s"

        params = [form.email.data]
        cur.execute(sql, params)
        result = cur.fetchall()
        print(result)
        print(check_password_hash(result[0][0], form.password.data))

        if check_password_hash(result[0][0], form.password.data) and result is not None:
            con.commit()
            con.close()
            return redirect(url_for('home'))
        else:
            message = "Incorrect password or email."
            return render_template('login.html', form=form, message=message)
    return render_template('login.html', form=form)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    message = None
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
