from database import db


class User(db.Model):
    user_id = db.Column("User_ID", db.Integer, primary_key=True)
    email = db.Column("Email", db.String(50))
    full_name = db.Column("Name", db.String(75))
    password = db.Column("Password", db.String(255))
    events_attending = db.relationship("RSVP", backref="user", lazy=True)

    def __init__(self, id, email, full_name, password):
        self.user_id = id
        self.email = email
        self.full_name = full_name
        self.password = password

class Event(db.Model):
    event_id = db.Column("Event_ID", db.Integer, primary_key=True)
    date = db.Column("Date", db.String(10))
    name = db.Column("Name", db.String(75))
    rating = db.Column("Rating", db.Float)
    user = db.Column("User", db.String(50))
    reports = db.Column("Reports", db.Integer)
    desc = db.Column("Description", db.String(500))
    likes = db.Column("Likes", db.Integer)
    events_attending = db.relationship("RSVP", backref="event",cascade="all, delete-orphan", lazy=True)

    def __init__(self, event_id, date, name, rating, user, reports, desc, likes):
        self.event_id = event_id
        self.date = date
        self.name = name
        self.rating = rating
        self.user = user
        self.reports = reports
        self.desc = desc
        self.likes = likes

class RSVP(db.Model):
    RSVP_id = db.Column("RSVP_ID", db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.Event_ID"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.User_ID"))

    def __init__(self, id, event_id, user_id):
        self.RSVP_id = id
        self.event_id = event_id
        self.user_id = user_id
