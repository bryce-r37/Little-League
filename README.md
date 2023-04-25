# Little-League

## Intro to Databases Final Project
Team Members:
- Bryce Robinson
- Carson Buntin
- Michael Mathews

## Virtual Environment Setup
In project directory, run the follwoing.
```
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install flask-wtf
pip install email-validator
pip install flask-login
pip install python-dotenv
pip install pymysql
pip install werkzeug
```

## Python Modules Imported
```
flask
flask-wtf
flask-login
email-validator
pymysql
werkzeug
```

## Accessing Website
1. Import **littleleague.sql** into a MariaDB database.
1. Modify **csi3335sp2023.py** to set correct values in the *sql* dictionary.
1. Configure python virtual environment with necessary [modules](#Python%20Modules%20Imported).
1. Run the command `export FLASK_APP=little-league.py`.
1. Run the command `flask run` to start the web app.
1. Go to <http://127.0.0.1/5000> to view the website.

## Website Features
- Secure Login
- Team batting and pitching stats for each year up to 2021
- Career stats for each player linked from team stats page
- Request logging for each user viewable by admin user

## Admin Login Credentials
**Username:** Little-League-Admin
**Password:** TigersRule23

