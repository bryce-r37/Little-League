# file: sql.py
# authors: Carson Buntin, Bryce Robinson
# date: 4/24/23

import pymysql
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from csi3335sp2023 import mysql

con = pymysql.connect(host=mysql['location'], 
                      user=mysql['user'], 
                      password=mysql['password'], 
                      database=mysql['database'])
cur = con.cursor()

def ValidateLogin(form):
   sql = "SELECT password FROM user WHERE email = %s OR username = %s"

   params = [form.email.data.lower(), form.email.data]
   cur.execute(sql, params)

   result = cur.fetchall()

   if result:
      if check_password_hash(result[0][0], form.password.data):
         con.commit()
         return "Success"
      else:
         return "Incorrect password."
   else:
      return "Email/Username not found."


def CreateAccount(form):
   sql = "INSERT INTO user (email, username, name, password) VALUES (%s, %s, %s, %s)"
   passwordHash = generate_password_hash(form.password.data)
   name = form.nameF.data + " " + form.nameL.data

   params = [form.email.data.lower(), form.username.data, name, passwordHash]

   try:
      cur.execute(sql, params)
      con.commit()
      return "Success"
   except IntegrityError as e:
      if 'PRIMARY' in str(e):
         return 'Email already exists. Please choose a different email.'
      else:
         return 'Username already exists. Please choose a different username.'


def FetchPitching(team, year):
   sql = "SELECT playerid, concat(nameFirst, ' ', nameLast), p_G, p_GS, round(p_IPOuts / 3, 5), round(3 * (p_BB + p_H) / p_IPOuts, 5), round(p_SO / (p_IPOuts / 3), 5) FROM pitching NATURAL JOIN people WHERE teamID = %s AND yearID = %s"
   params = [team, year]

   cur.execute(sql, params)

   return cur.fetchall()


def FetchBatting(team, year):
   sql = "SELECT concat(nameFirst, ' ', nameLast) as Player, b_G FROM batting NATURAL JOIN people WHERE teamID = %s AND yearID = %s"
   params = [team, year]

   cur.execute(sql, params)

   return cur.fetchall()

def FetchPlayer(playerid):
   sql = "SELECT concat(nameFirst, ' ', nameLast) FROM people WHERE playerid = %s"
   params = [playerid]

   cur.execute(sql, params)
   
   return cur.fetchall()[0]
