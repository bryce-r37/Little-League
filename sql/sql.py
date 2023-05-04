# file: sql.py
# authors: Carson Buntin, Bryce Robinson
# date: 4/24/23

import pymysql
from datetime import datetime
from flask_login import current_user
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


def FetchUser(user):
    sql = "SELECT username, team FROM user WHERE email = %s OR username = %s"

    params = [user, user]
    cur.execute(sql, params)

    return cur.fetchone()


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


def FetchAllYears():
    sql = "SELECT DISTINCT yearID FROM teams"
    cur.execute(sql)
    return cur.fetchall()


def FetchYears(team):
    sql = "SELECT yearID FROM teams WHERE team_name = %s"
    params = [team]
    cur.execute(sql, params)
    return cur.fetchall()


def FetchTeamID(team, yearid):
    sql = "SELECT DISTINCT teamID FROM teams WHERE team_name = %s AND yearID = %s"
    params = [team, yearid]
    cur.execute(sql, params)

    teamID = cur.fetchall()
    print(teamID)
    return str(teamID[0][0])


def FetchTeamName(teamID, yearid):
    sql = "SELECT DISTINCT team_name FROM teams WHERE teamid = %s AND yearID = %s"
    params = [teamID, yearid]
    cur.execute(sql, params)

    team = cur.fetchall()
    return str(team[0][0])


def FetchCurrentTeams(yearID):
    sql = "SELECT DISTINCT team_name from teams WHERE yearID = %s"
    params = [yearID]
    cur.execute(sql, params)

    teams = cur.fetchall()
    return teams


def ChangeBackground(team):
    sql = "UPDATE user SET team = (SELECT DISTINCT teamID FROM teams WHERE team_Name = %s AND yearID = 2022) WHERE username = %s"
    params = [team, current_user.username]
    cur.execute(sql, params)
    return cur.fetchall()


def FetchPitching(team, year):
    sql = "SELECT playerid, concat(IFNULL(nameFirst, ''), ' ', " \
          "IFNULL(nameLast, '')), p_G, p_GS, " \
          "round(p_IPOuts / 3, 3), round(3 * (p_BB + p_H) / p_IPOuts, 3), " \
          "round(p_SO / (p_IPOuts / 3), 3), round(p_ERA, 2) " \
          "FROM pitching NATURAL JOIN people " \
          "WHERE teamID = %s AND yearID = %s"
    params = [team, year]

    cur.execute(sql, params)

    return cur.fetchall()


def FetchBatting(team, year):
    sql = "SELECT playerid, concat(IFNULL(nameFirst, ''), ' ', " \
          "IFNULL(nameLast, '')) AS name, sum(IFNULL(G_p, 0)), " \
          "sum(IFNULL(G_c, 0)), sum(IFNULL(G_1b, 0)), sum(IFNULL(G_2b, 0)), " \
          "sum(IFNULL(G_3b, 0)), sum(IFNULL(G_ss, 0)), sum(IFNULL(G_lf, 0)), " \
          "sum(IFNULL(G_cf, 0)), sum(IFNULL(G_rf, 0)), sum(IFNULL(G_of, 0)), " \
          "sum(IFNULL(G_dh, 0)), sum(IFNULL(G_ph, 0)), sum(IFNULL(G_pr, 0)), " \
          "sum(b_AB) AS AB, round(IFNULL(sum(b_H)/sum(b_AB), 0), 3) AS AVG, " \
          "round(IFNULL((sum(b_H)+sum(b_BB)+sum(b_HBP))/(sum(b_AB)+sum(b_BB)+" \
          "sum(b_HBP)+sum(b_SF)), 0), 3) AS OBP, " \
          "round(IFNULL(((sum(b_H)-sum(b_2B)-sum(b_3B)-sum(b_HR))+(2*sum(b_2B))+" \
          "(3*sum(b_3B))+(4*sum(b_HR)))/sum(b_AB), 0), 3) AS SLG " \
          "FROM batting NATURAL JOIN people NATURAL JOIN appearances " \
          "WHERE teamid = %s AND yearid = %s AND NOT b_AB = 0 GROUP BY playerid"

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
    sql = "SELECT concat(IFNULL(nameFirst, ''), ' ', IFNULL(nameLast, '')), " \
          "team_name, yearid, " \
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


def FetchAllPitching(year):
    sql = "SELECT playerid, concat(IFNULL(nameFirst, ''), ' ', " \
          "IFNULL(nameLast, '')), sum(p_G), sum(p_GS), " \
          "round(sum(p_IPOuts) / 3, 3), round(3 * (sum(p_BB) + sum(p_H)) / sum(p_IPOuts), 3), " \
          "round(sum(p_SO) / (sum(p_IPOuts) / 3), 3), round(sum(p_ERA), 2) " \
          "FROM pitching NATURAL JOIN people " \
          "WHERE yearID = %s GROUP BY playerid"
    params = [year]

    cur.execute(sql, params)

    return cur.fetchall()


def FetchAllBatting(year):
    sql = "SELECT playerid, concat(IFNULL(nameFirst, ''), ' ', " \
          "IFNULL(nameLast, '')) AS name, sum(IFNULL(G_p, 0)), " \
          "sum(IFNULL(G_c, 0)), sum(IFNULL(G_1b, 0)), sum(IFNULL(G_2b, 0)), " \
          "sum(IFNULL(G_3b, 0)), sum(IFNULL(G_ss, 0)), sum(IFNULL(G_lf, 0)), " \
          "sum(IFNULL(G_cf, 0)), sum(IFNULL(G_rf, 0)), sum(IFNULL(G_of, 0)), " \
          "sum(IFNULL(G_dh, 0)), sum(IFNULL(G_ph, 0)), sum(IFNULL(G_pr, 0)), " \
          "sum(b_AB) AS AB, round(IFNULL(sum(b_H)/sum(b_AB), 0), 3) AS AVG, " \
          "round(IFNULL((sum(b_H)+sum(b_BB)+sum(b_HBP))/(sum(b_AB)+sum(b_BB)+" \
          "sum(b_HBP)+sum(b_SF)), 0), 3) AS OBP, " \
          "round(IFNULL(((sum(b_H)-sum(b_2B)-sum(b_3B)-sum(b_HR))+(2*sum(b_2B))+" \
          "(3*sum(b_3B))+(4*sum(b_HR)))/sum(b_AB), 0), 3) AS SLG " \
          "FROM batting NATURAL JOIN people NATURAL JOIN appearances " \
          "WHERE yearid = %s AND b_AB != 0 GROUP BY playerid" 

    params = [year]

    cur.execute(sql, params)

    results = list(cur.fetchall())

    for i in range(len(results)):
        temp = list(results[i])
        for j in range(len(temp)):
            if temp[j] is None:
                temp[j] = 0
        results[i] = tuple(temp)

    return tuple(results)


def PostRequest(user, team, year):
    sql = "INSERT INTO userquery (username, team, year, datetime) VALUES " \
          "(%s, %s, %s, %s)"

    params = [user, team, year, datetime.today()]

    cur.execute(sql, params)

    con.commit()


def CountRequests():
    sql = "SELECT count(username) FROM userquery"

    cur.execute(sql)

    return cur.fetchone()[0]


def FetchRequests():
    sql = "SELECT username, team, year, datetime FROM userquery"

    cur.execute(sql)

    return cur.fetchall()
