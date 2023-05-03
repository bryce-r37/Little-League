# file: routes.py
# authors: Bryce Robinson, Carson Buntin
# date: 4/18/23

from flask import render_template, flash, redirect, url_for, jsonify, request, make_response
from flask_login import current_user, login_user, login_required, logout_user

from app import app, login
from app.forms import LoginForm, CreateAccountForm
from app.models import User

from sql import sql
from sql.sql import ValidateLogin, CreateAccount, FetchPitching, FetchBatting, \
    FetchPlayer, FetchTeams, FetchYears, FetchAllYears, FetchTeamID, FetchTeamName, \
    FetchAllPitching, FetchAllBatting, FetchUser, FetchCurrentTeams, ChangeBackRound


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teams', methods=['GET', 'POST'])
@login_required
def home():
    teams = FetchTeams()
    if request.method == 'POST':
        team = request.form.get('team')
        year = request.form.get('year')
        team = FetchTeamID(team, year)
        return redirect(url_for('pitching', teamID=team, year=year))
    return render_template('home.html', title='Team Select', teams=teams)


@app.route('/years/<team>')
@login_required
def years(team):
    team = team.replace('-', '/')
    teamYears = FetchYears(team)
    return jsonify(teamYears)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        message = ValidateLogin(form)
        if message == "Success":
            user = FetchUser(form.email.data)
            user = User(user[0], user[1])
            login_user(user)
            return redirect(url_for('home'))
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
@login_required
def pitching(teamID, year):
    name = FetchTeamName(teamID, year)
    return render_template('pitching.html', title='Team Stats', team=teamID, year=year,
                           name=name, page="Pitching", players=FetchPitching(teamID, year))


@app.route('/stats/<teamID>/<year>/batting')
@login_required
def batting(teamID, year):
    name = FetchTeamName(teamID, year)
    return render_template('batting.html', title='Team Stats', team=teamID, year=year,
                           name=name, page="Batting", players=FetchBatting(teamID, year))


@app.route('/player/<playerid>')
@login_required
def player(playerid):
    return render_template('player.html', title='Player Stats',
                           stints=FetchPlayer(playerid))


@login_required
@app.route('/pitchers')
def allPitchers():
    allYears = FetchAllYears()
    allYears = sorted([str(y[0]) for y in allYears], reverse=True)
    year = request.args.get('year', '2022')
    players = FetchAllPitching(year)
    return render_template('allPitchers.html', title='All Pitchers', players=players, years=allYears,
                           selected_year=year)


@app.route('/batters')
@login_required
def allBatters():
    allYears = FetchAllYears()
    allYears = sorted([str(y[0]) for y in allYears], reverse=True)
    year = request.args.get('year', '2022')
    players = FetchAllBatting(year)
    return render_template('allBatters.html', title='All Batters', players=players, years=allYears, 
                           selected_year=year)


@app.route('/background')
@login_required
def background():
    currentTeams = FetchCurrentTeams("2022")
    return render_template('background.html', title='Background', teams=currentTeams)


@app.route('/admin')
@login_required
def admin():
    if current_user.username != 'Little-League-Admin':
        return redirect(url_for('home'))
    return render_template('admin.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update-team/<team>', methods=['GET'])
def update_team(team):
    result = ChangeBackRound(team=team)

    return redirect(url_for('background'))
