# file: __init__.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
