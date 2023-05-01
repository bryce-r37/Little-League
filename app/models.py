from flask_login import UserMixin
from app import login

class User(UserMixin):
    def __init__(self, username):
        self.username=username
        self.id=username

@login.user_loader
def load_user(id):
    return User(id)
