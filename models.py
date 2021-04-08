from database import db


class User(db.Model):
    email = db.Column("Email", db.String(50), primary_key=True)
    full_name = db.Column("Name", db.String(75))
    password = db.Column("Password", db.String(100))

    def __init__(self, email, full_name, password):
        self.email = email
        self.full_name = full_name
        self.password = password


class Event(db.Model):
    event_id = db.Column("ID", db.Integer(10))
    date =  db.Column("Date", db.String(10))
    name = db.Column("Name", db.String(75))
    rating = db.Column("Rating", db.Integer(1))
    user = db.Column("User", db.String(50))
    reports = db.Column("Reports", db.Integer(2))
    desc = db.Column("Description", db.String(500))
    def __init__(self,event_id, date,name,rating,user,reports,desc):
        self.event_id = event_id
        self.date = date
        self.name = name
        self.rating = rating
        self.user = user
        self.reports = reports
        self.desc = desc