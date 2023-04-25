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
        sql = "SELECT password FROM user WHERE email = %s OR username = %s"

        params = [form.email.data.lower(), form.email.data]
        cur.execute(sql, params)
        result = cur.fetchall()

        if result:
            if check_password_hash(result[0][0], form.password.data):
                con.commit()
                return redirect(url_for('home'))
            else:
                message = "Incorrect password or Username/Email"
                return render_template('login.html', form=form, message=message)
        else:
            message = "Email/Username not found."
            return render_template('login.html', form=form, message=message)
    return render_template('login.html', form=form)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    message = None
    if form.validate_on_submit():
        sql = "INSERT INTO user (email, username, name, password) VALUES (%s, %s, %s, %s)"
        passwordHash = generate_password_hash(form.password.data)
        name = form.nameF.data + " " + form.nameL.data

        params = [form.email.data.lower(), form.username.data, name, passwordHash]
        try:
            cur.execute(sql, params)
            con.commit()
            return redirect(url_for('home'))
        except IntegrityError as e:
            if 'PRIMARY' in str(e):
                message1 = 'Email already exists. Please choose a different email.'
                return render_template('createAccount.html', form=form, message1=message1)
            else:
                message2 = 'Username already exists. Please choose a different username.'
                return render_template('createAccount.html', form=form, message2=message2)

    return render_template('createAccount.html', form=form)
