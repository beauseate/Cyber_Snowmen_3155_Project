from database import db


class User(db.Model):
    email = db.Column("Email", db.String(50), primary_key=True)
    f_name = db.Column("First Name", db.String(50))
    password = db.Column("Password", db.String(100))
    # Need to add a column for events attending/liked


class Events(db.Model):
    # Just added this here as a template for later
    pass
