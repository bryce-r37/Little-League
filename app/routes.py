# file: routes.py
# authors: Bryce Robinson, Carson Buntin
# date: 4/18/23

from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user

from app import app
from app.forms import LoginForm, CreateAccountForm

from sql import sql
from sql.sql import ValidateLogin, CreateAccount, FetchPitching, FetchBatting, FetchPlayer, FetchTeams, FetchYears


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    teams = FetchTeams()
    if request.method == 'POST':
        print("test")
        team = request.form.get('team')
        year = request.form.get('year')
        # do something with the team and year values
        return render_template('pitching.html', title='Stats', team=team, year=year,
                               players=FetchPitching(team, year))
    return render_template('home.html', title='Home', teams=teams)


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


@app.route('/team/pitching')
def pitching():
    team = 'DET'
    year = '2020'
    return render_template('pitching.html', title='Stats', team=team, year=year,
                           players=FetchPitching(team, year))


@app.route('/team/batting')
def batting():
    team = 'DET'
    year = '2020'
    return render_template('batting.html', title='Stats', team=team, year=year,
                           players=FetchBatting(team, year))


@app.route('/player/<playerid>/<table>')
def player(playerid, table):
    return render_template('player.html', title='Player Stats',
                           stints=FetchPlayer(playerid), table=table)
