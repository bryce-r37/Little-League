# file: routes.py
# authors: Bryce Robinson, Carson Buntin
# date: 4/18/23

from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user

from app import app
from app.forms import LoginForm, CreateAccountForm

from sql import sql
from sql.sql import ValidateLogin, CreateAccount, FetchPitching, FetchBatting, \
        FetchPlayer, FetchTeams, FetchYears, FetchTeamID, FetchTeamName, \
        FetchAllPitching, FetchAllBatting


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/teams', methods=['GET', 'POST'])
def home():
    teams = FetchTeams()
    if request.method == 'POST':
        team = request.form.get('team')
        year = request.form.get('year')
        team = FetchTeamID(team, year)
        return redirect(url_for('pitching', teamID=team, year=year))
    return render_template('home.html', title='Team Select', teams=teams)


@app.route('/years/<team>')
def years(team):
    teamYears = FetchYears(team)
    return jsonify(teamYears)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        message = ValidateLogin(form)
        if message == "Success":
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form, message=message)
    return render_template('login.html', form=form)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        message = CreateAccount(form)
        if message == "Success":
            return redirect(url_for('home'))
        else:
            return render_template('createAccount.html', form=form, message=message)
    return render_template('createAccount.html', form=form)


@app.route('/stats/<teamID>/<year>/pitching')
def pitching(teamID, year):
    name = FetchTeamName(teamID, year)
    return render_template('pitching.html', title='Team Stats', team=teamID, year=year,
                           name=name, players=FetchPitching(teamID, year))


@app.route('/stats/<teamID>/<year>/batting')
def batting(teamID, year):
    name = FetchTeamName(teamID, year)
    return render_template('batting.html', title='Team Stats', team=teamID, year=year,
                           name=name, players=FetchBatting(teamID, year))


@app.route('/player/<playerid>')
def player(playerid):
    return render_template('player.html', title='Player Stats',
                           stints=FetchPlayer(playerid))


@app.route('/pitchers')
def allPitchers():
   year = 2021
   players = FetchAllPitching(year)
   return render_template('allPitchers.html', title1='All Pitchers', players=players)


@app.route('/batters')
def allBatters():
   year = 2021
   players = FetchAllBatting(year)
   return render_template('allBatters.html', title='All Batters', players=players)


@app.route('/admin')
def admin():
   return render_template('admin.html')
