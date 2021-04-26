from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db
import re


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    first_name = StringField('First Name', validators=[Length(1, 10)])

    last_name = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', validators=[
        DataRequired()])

    password = PasswordField('Password', validators=[
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
        if re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', field.data) is None:
            raise ValidationError('Not a valid email address.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', validators=[
        DataRequired()])

    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')
        if re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', field.data) is None:
            raise ValidationError('Not a valid email address.')


class NewEventForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Event Name', validators=[DataRequired("Please enter a name for the event."), Length(1, 500)])
    desc = StringField('Description', validators=[DataRequired("Please enter a description for the event."),
                                                  Length(1, 500)])
    date = DateField('Date (Enter in the format of YYYY-MM-DD)', format='%Y-%m-%d',
                     validators=[DataRequired("Please enter a valid date.")])

    submit = SubmitField('Submit')

    def validate_date(self, field):
        # Get form date as a String and assign its value to year, month, and day for validation
        tempDate = field.data.strftime('%Y-%m-%d')
        year = tempDate[0:4]
        month = tempDate[5:7]
        day = tempDate[8:10]

        # Cast date values into int for validation
        month = int(month)
        day = int(day)
        year = int(year)
        # Ensure that events are created only for future dates
        if year < 2021 or (year == 2021 and month < 4):
            raise ValidationError('It has to be an event in the future!')
        # Check for valid Feb dates on leap years
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if month == 2 and day > 29:
                raise ValidationError('Day cannot be greater than 29')
        else:
            if month == 2 and day > 28:
                raise ValidationError('Day cannot be greater than 28')

class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('Comment',validators=[Length(min=1)])

    submit = SubmitField('Add Comment')

