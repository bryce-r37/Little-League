from flask_login import UserMixin
from app import login
from sql import sql
from sql.sql import FetchUser

class User(UserMixin):
    def __init__(self, username, team):
        self.username=username
        self.team=team
        self.id=username

@login.user_loader
def load_user(id):
    user = FetchUser(id)
    return User(user[0], user[1])
