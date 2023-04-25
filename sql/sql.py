# file: sql.py
# authors: Carson Buntin, Bryce Robinson
# date: 4/24/23

import pymysql
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash

con = pymysql.connect(host='localhost', user='root', password='Cars0n200!', db='littleleauge')
cur = con.cursor()

def ValidateLogin(form):
   sql = "SELECT * FROM user WHERE email = %s AND password = %s"
   passwordHash = generate_password_hash(form.password.data)

   params = [form.email.data, passwordHash]
   cur.execute(sql, params)

   return cur.fetchAll()

def CreateAccount(form):
   sql = "INSERT INTO user (email, name, password) VALUES (%s, %s, %s)"
        passwordHash = generate_password_hash(form.password.data)
        name = form.nameF.data + " " + form.nameL.data

        params = [form.email.data, name, passwordHash]

        try:
            cur.execute(sql, params)
            con.commit()
            con.close()
            return True
        except IntegrityError:
            return False
