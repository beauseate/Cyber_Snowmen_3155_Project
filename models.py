from database import db


class User(db.Model):
    email = db.Column("Email", db.String(50), primary_key=True)
    full_name = db.Column("Name", db.String(75))
    password = db.Column("Password", db.String(100))
    # Need to add a column for events attending/liked

    def __init__(self, email, full_name, password):
        self.email = email
        self.full_name = full_name
        self.password = password
