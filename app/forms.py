# file: forms.py
# authors: Bryce Robinson
# date: 4/22/23

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length


class CreateAccountForm(FlaskForm):
    nameF = StringField('First Name', validators=[DataRequired()])
    nameL = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email("Please enter a valid Email", False, True)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Regexp("(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{1,100}",
                                                            0,
                                                            "Field must contain at least 1 uppercase, 1 lowercase, and 1 digit. "),
                                                     Length(8, 32)])
    passwordConf = PasswordField('Confirm Password',
                                 validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


