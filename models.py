from database import db


class User(db.Model):
    user_id = db.Column("User_ID", db.Integer, primary_key=True)
    email = db.Column("Email", db.String(50))
    first_name = db.Column("first_name", db.String(75))
    last_name = db.Column("Last_Name", db.String(75))
    password = db.Column("Password", db.String(255))
    events_liked = db.relationship("Likes", backref="user", cascade="all, delete-orphan", lazy=True)
    events_attending = db.relationship("RSVP", backref="user", lazy=True)
    comments = db.relationship("Comments", backref="user", lazy=True)

    def __init__(self, id, email, first_name, last_name, password):
        self.user_id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
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
    filename = db.Column("filename", db.String(150), nullable=False, server_default='default.png')

    user_id = db.Column(db.Integer(), db.ForeignKey("user.User_ID"), nullable=False)
    events_attending = db.relationship("RSVP", backref="event",cascade="all, delete-orphan", lazy=True)
    comments = db.relationship("Comments", backref="event", cascade="all, delete-orphan", lazy=True)

    def __init__(self, event_id, date, name, rating, user, reports, desc, likes, user_id, filename):
        self.event_id = event_id
        self.date = date
        self.name = name
        self.rating = rating
        self.user = user
        self.reports = reports
        self.desc = desc
        self.likes = likes
        self.user_id = user_id
        self.filename = filename

class RSVP(db.Model):
    RSVP_id = db.Column("RSVP_ID", db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.Event_ID"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.User_ID"))

    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id


class Likes(db.Model):
    likes_id = db.Column("Likes_ID", db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.Event_ID"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.User_ID"))

    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id

class Comments(db.Model):
    comment_id = db.Column("Comment_ID", db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.Event_ID"), nullable=False)
    first_name = db.Column(db.String, db.ForeignKey("user.first_name"))
    content = db.Column(db.VARCHAR, nullable=False)

    def __init__(self, event_id, content, first_name):
        self.event_id = event_id
        self.content = content
        self.first_name = first_name

