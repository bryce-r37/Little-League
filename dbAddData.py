import pymysql
from csi3335sp2023 import mysql
import csv

con = pymysql.connect(host=mysql['location'],
                      user=mysql['user'],
                      password=mysql['password'],
                      database=mysql['database'])
cur = con.cursor()

with open('baseballdatabank-2023.1/core/people.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO people (playerID, birthYear, birthMonth, birthDay, birthCountry, 
                                    birthState, birthCity, deathYear, deathMonth, deathDay, 
                                    deathCountry, deathState, deathCity, nameFirst, nameLast, 
                                    nameGiven, weight, height, bats, throws, debutDate, finalGameDate, 
                                    retroID, bbrefID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[20][:4]
        if year == "2022":
            row = [None if x == "" else x for x in row]
            cur.execute(sql, row)

    con.commit()


with open('baseballdatabank-2023.1/core/Pitching.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO pitching (playerID, yearID, teamID, stint, p_W, 
                                    p_L, p_G, p_GS, p_CG, p_SHO, p_SV, p_IPOuts, 
                                    p_H, p_ER, p_HR, p_BB, p_SO, p_BAOpp, p_ERA, 
                                    p_IBB,p_WP, p_HBP, p_BK, p_BFP, p_GF, p_R, p_SH, 
                                    p_SF, p_GIDP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[1]
        params = [row[0], row[1], row[3], row[2], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24],row[25], row[26], row[27], row[28], row[29]]
        if year == "2022":
            row = [None if x == "" else x for x in row]
            cur.execute(sql, params)

    con.commit()

with open('baseballdatabank-2023.1/core/Batting.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO batting (playerID, yearId, teamID, stint, b_G, 
                                    b_AB, b_R, b_H, b_2B, b_3B, b_HR, b_RBI, 
                                    b_SB, b_CS, b_BB, b_SO, b_IBB, b_HBP, b_SH, 
                                    b_SF, b_GIDP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[1]
        params = [row[0], row[1], row[3], row[2], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21]]
        if year == "2022":
            row = [None if x == "" else x for x in row]
            cur.execute(sql, params)

    con.commit()

with open('baseballdatabank-2023.1/core/Appearances.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO appearances (playerID, yearID, teamId, G_all, GS, G_batting, G_defense, 
                                        G_p, G_c, G_1b, G_2b, G_3b, G_ss, G_lf, G_cf, 
                                        G_rf, G_of, G_dh, G_ph, G_pr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[0]
        params = [row[3], row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
        if year == "2022":
            row = [None if x == "" else x for x in row]
            cur.execute(sql, params)

    con.commit()

with open('baseballdatabank-2023.1/core/Teams.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO teams (teamID, yearID, lgID, divID, franchID, team_name, 
                                        team_rank, team_G, team_G_home, team_W, team_L, 
                                        DivWin, WCWin, LgWin, WSWin, team_R, team_AB, team_H, 
                                        team_2B, team_3B, team_HR, team_BB, team_SO, team_SB, 
                                        team_CS, team_HBP, team_SF, team_RA, team_ER, team_ERA, 
                                        team_CG, team_SHO, team_SV, team_IPouts, team_HA, team_HRA, 
                                        team_BBA, team_SOA, team_E, team_DP, team_FP, park_name, 
                                        team_attendance, team_BPF, team_PPF) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[0]
        params = [row[2], row[0], row[1], row[4], row[3], row[40], row[5], row[6], row[7], row[8], row[9], row[10],
                  row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21],
                  row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32],
                  row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[41], row[42], row[43], row[44]]

        if year == "2022":
            row = [None if x == "" else x for x in row]
            cur.execute(sql, params)

    con.commit()

with open('baseballdatabank-2023.1/contrib/AwardsPlayers.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    sql = '''INSERT INTO awards (award_name, yearID, 
                                playerID, lgID, tie, notes) VALUES (%s, %s, %s, %s, %s, %s)'''

    for row in csvreader:
        year = row[2]
        params = [row[1], row[2], row[0], row[3], row[4], row[5]]

        if year == "2022":
            print(year)
            row = [None if x == "" else x for x in row]
            cur.execute(sql, params)

    con.commit()