# file: __init__.py
# authors: Bryce Robinson
# date: 4/18/23

from flask import Flask

app = Flask(__name__)

from app import routes
