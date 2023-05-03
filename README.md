# Little League

## Intro to Databases Final Project
Team Members:
- Bryce Robinson
- Carson Buntin
- Michael Mathews

## Virtual Environment Setup
In the project directory, run the following Bash commands.
```
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install flask-wtf
pip install flask-login
pip install email-validator
pip install pymysql
pip install werkzeug
pip install python-dotenv
```
_Note: `python-dotenv` is an optional module, and not necessary for the application to function. It simply removes the need to run `export FLASK_APP` at the beginning of every terminal session by automatically importing environment variables stored in **.flaskenv** at runtime._

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
1. Import **littleleague.sql** into a MariaDB relational database.
1. Modify **csi3335sp2023.py** and set *username*, *password*, and *database* values in the *sql* dictionary to connect to your local MariaDB database.
1. Configure a python virtual environment with the necessary [python modules](#python-modules-imported).
1. Activate the virtual environment.
1. Ensure that the database is running.
1. In Bash/Zsh, run the command `export FLASK_APP=little-league.py` to set the *App* variable.
1. In Bash/Zsh, run the command `flask run` to start the web app.
1. Go to <http://127.0.0.1/5000> (or the link provided by Flask) to view the website.
   1. Create a new account or log in to an existing user/admin account to view statistics.

## Website Features
- Secure login with password encryption
- Team batting and pitching stats for each year up to 2022 with search and filter
- Career stats for each player linked from team stats page
- Request logging for each user viewable by admin
- All batting and pitching stats for each year with search and filter
- Custom MLB team backgrounds linked to user profiles

## Admin Login Credentials
**Username:** Little-League-Admin

**Password:** TigersRule23

## MLB Backgrounds
- Artwork is not owned by Little League
- Artwork is intended only for private/personal use
- No profits were made off of artwork (except for hopefully a few extra credit points)

## Extra Features
All
   - Attractive UI (tables, buttons, font, tabs, background)
Create Account
   - Validation that there is input for each field
   - Extra validation for email, password, and that both passwords match
Pitchers
   - Search functionality
   - Sort by statistic functionality
   - Show x amount of entries and multiple pages
   - Link to each player
   - ERA column
Batters
   - Search functionality
   - Sort by statistic functionality
   - Show x amount of entries and multiple pages
   - Link to each player
   - AB column
All Pitchers/Batters
   - All Pitchers by year page
   - All Batters by year page
   - Search functionality
   - Sort by statistic functionality
   - Link to each player
   - Show x amount of entries and multiple pages
Players
   - Shows each player, their stints, and ther stats per stint
   - Link to each stint with specific team
My Team Tab
   - Ability to set background for selected favorite current team
   - Favorite team background is automatically displayed on user login
Log Out functionality