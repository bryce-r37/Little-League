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


def FetchTeams():
    sql = "SELECT DISTINCT team_name FROM teams ORDER BY team_name"
    cur.execute(sql)
    return cur.fetchall()


def FetchYears(team):
    sql = "SELECT yearID FROM teams WHERE team_name = %s"
    params = [team]
    cur.execute(sql, params)
    return cur.fetchall()


def FetchTeamID(team):
    sql = "SELECT DISTINCT teamID FROM teams WHERE team_name = %s"
    params = [team]
    cur.execute(sql, params)

    teamID = cur.fetchall()
    return str(teamID[0][0])


def FetchTeamName(teamID):
   sql = "SELECT DISTINCT team_name FROM teams WHERE teamid = %s"
   params = [teamID]
   cur.execute(sql, params)

   team = cur.fetchall()
   return str(team[0][0])


def FetchPitching(team, year):
    sql = "SELECT playerid, concat(nameFirst, ' ', nameLast), p_G, p_GS, " \
          "round(p_IPOuts / 3, 3), round(3 * (p_BB + p_H) / p_IPOuts, 3), " \
          "round(p_SO / (p_IPOuts / 3), 3), round(p_ERA, 2) " \
          "FROM pitching NATURAL JOIN people " \
          "WHERE teamID = %s AND yearID = %s"
    params = [team, year]

    cur.execute(sql, params)

    return cur.fetchall()


def FetchBatting(team, year):
    sql = "SELECT playerid, name, AVG, OBP, SLG, P, C, " \
          "1B, 2B, 3B, SS, LF, CF, RF, OF FROM " \
          "(SELECT playerid, concat(nameFirst, ' ', nameLast) AS name, " \
          "teamid, yearid, round(IFNULL(b_H/b_AB, 0), 3) AS AVG, " \
          "round(IFNULL((b_H+b_BB+b_HBP)/(b_AB+b_BB+b_HBP+b_SF), 0), 3) AS OBP, " \
          "round(IFNULL(((b_H-b_2B-b_3B-b_HR)+(2*b_2B)+(3*b_3B)+(4*b_HR))/b_AB, 0), 3) AS SLG " \
          "FROM batting NATURAL JOIN people " \
          "WHERE teamid = %s AND yearid = %s AND b_AB != 0) ta " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'P' FROM fielding " \
          "WHERE position = 'P') tb USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'C' FROM fielding " \
          "WHERE position = 'C') tc USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS '1B' FROM fielding " \
          "WHERE position = '1B') td USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS '2B' FROM fielding " \
          "WHERE position = '2B') te USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS '3B' FROM fielding " \
          "WHERE position = '3B') tf USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'SS' FROM fielding " \
          "WHERE position = 'SS') tg USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'LF' FROM fielding " \
          "WHERE position = 'LF') th USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'CF' FROM fielding " \
          "WHERE position = 'CF') ti USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'RF' FROM fielding " \
          "WHERE position = 'RF') tj USING (playerid, teamid, yearid) " \
          "LEFT JOIN (SELECT playerid, teamid, yearid, f_G AS 'OF' FROM fielding " \
          "WHERE position = 'OF') tk USING (playerid, teamid, yearid)"

    params = [team, year]

    cur.execute(sql, params)

    results = list(cur.fetchall())

    for i in range(len(results)):
        temp = list(results[i])
        for j in range(len(temp)):
            if temp[j] is None:
                temp[j] = 0
        results[i] = tuple(temp)

    return tuple(results)


def FetchPlayer(playerid):
    sql = "SELECT concat(nameFirst, ' ', nameLast), team_name, yearid, " \
          "b_G, round(IFNULL(b_H/b_AB, 0), 3), " \
          "round(IFNULL((b_H+b_BB+b_HBP)/(b_AB+b_BB+b_HBP+b_SF), 0), 3), " \
          "round(IFNULL(((b_H-b_2B-b_3B-b_HR)+(2*b_2B)+(3*b_3B)+(4*b_HR))/b_AB, 0), 3), " \
          "round(IFNULL(p_ERA, 0), 2), teamid " \
          "FROM people NATURAL JOIN batting JOIN teams USING (teamid, yearid) " \
          "LEFT JOIN pitching USING (playerid, yearid, teamid, stint) " \
          "WHERE playerid = %s"
    params = [playerid]

    cur.execute(sql, params)

    return cur.fetchall()
