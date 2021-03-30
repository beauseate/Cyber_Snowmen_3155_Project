from database import db


class User(db.Model):
    email = db.Column("Email", db.String(50), primary_key=True)
    f_name = db.Column("First Name", db.String(50))
    password = db.Column("Password", db.String(100))
    # Need to add a column for events attending/liked

    def __init__(self, email, f_name, password):
        self.email = email
        self.f_name = f_name
        self.password = password
