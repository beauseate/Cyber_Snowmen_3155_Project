import pandas as pd
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    first_name = StringField('First Name', validators=[Length(1, 10)])

    last_name = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')


class NewEventForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Event_Name', [DataRequired("Please enter a name for the event,"), Length(1, 500)])
    desc = StringField('Description', [DataRequired("Please enter a description for the event,"), Length(1, 500)])
    date = DateField('Date (Enter in the format of YYYY-MM-DD)', format='%Y-%m-%d',
                     validators=[DataRequired("Please enter a date.")])

    def validate_date(self, field):
        year = field.data.strftime('%Y')
        month = field.data.strftime('%m')
        day = field.data.strftime('d')
        try:
            month = int(month)
            day = int(day)
            year = int(year)
        except ValueError:
            raise ValidationError('Date cannot contain characters other than 0-9 or -')
        if month < 1 or month > 12:
            raise ValidationError('Month has to be between 01 and 12')
        if year < 2021 or (year == 2021 and month < 4):
            raise ValidationError('It has to be an event in the future!')
        if day < 0 or day > 31:
            raise ValidationError('Day must be between 0 and 31')
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if day > 29:
                raise ValidationError('Day cannot be greater than 29')
            else:
                if day > 28:
                    raise ValidationError('Day cannot be greater than 28')
        if month == 4 or month == 6 or month == 9 or month == 11:
            if day > 30:
                raise ValidationError('Day cannot be greater than 30')
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if day > 31:
                raise ValidationError('Day cannot be greater than 31')

    submit = SubmitField('Submit')
