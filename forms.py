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

    name = StringField('Event_Name', [DataRequired("Please enter a name for the event,"), Length(1,500)])
    desc = StringField('Description', [DataRequired("Please enter a description for the event,"), Length(1, 500)])
    date = DateField('Date', format = '%m/%d/%y'[DataRequired("Please enter a date.")])

    def validate_date(self, field):
        datesList = pd.date_range(start=datetime.today(), end="2030-12-31").to_list()
        if not (field.data in datesList):
            raise ValidationError('Invalid date entered.')

    submit = SubmitField('Submit')