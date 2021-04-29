import os  # os is used to get environment variables IP & PORT

import bcrypt
from flask import Flask, flash  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from sqlalchemy import or_, func
from flask import get_flashed_messages

from database import db
from models import User as User, Likes, RSVP, Comments, Rating, Reports
from models import Event as Event
from random import randint
from flask import session
from forms import RegisterForm, LoginForm, NewEventForm, CommentForm
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
Images = join(dirname(realpath(__file__)),'Static\Images')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

app.config['UPLOAD_FOLDER'] = Images
db.init_app(app)
with app.app_context():
    db.create_all()

'''

TAB: HOME

DESC: The initial page of an existing and new user.

'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searchEvent = request.form['event']
        # Filters the Event table by Name attribute that is LIKE whatever the user searches
        events = Event.query.filter(or_(Event.name.ilike(f'%{searchEvent}%'), Event.desc.ilike(f'%{searchEvent}%'),
                                    Event.user.ilike(f'%{searchEvent}%'), Event.date.ilike(f'%{searchEvent}%')))
        if session.get('user'):
            return render_template('Home.html', events=events, user=session['user'])
        else:
            return render_template('Home.html', events=events)
    # Now sends list of all events to homepage
    if session.get('user'):
        listEvents = db.session.query(Event).all()
        return render_template('Home.html', events=listEvents, user=session['user'])
    else:
        listEvents = db.session.query(Event).all()
        return render_template('Home.html', events=listEvents)

'''

DESC: The route to each individual event filtered by it's event ID.

'''
@app.route('/events/<e_id>', methods = ['GET', 'POST'])
def get_event(e_id):
    eventExists = db.session.query(Event).filter_by(event_id=e_id).first()
    if session.get('user') and eventExists:
        # Check to see if the user has already liked this event
        hasFavorited = db.session.query(Event, Likes).filter(eventExists.event_id == Likes.event_id
                                                      ).filter(session['user_id'] == Likes.user_id).first()
        #check for reported status
        hasReported = db.session.query(Event, Reports).filter(eventExists.event_id == Reports.event_id
                                                      ).filter(session['user_id'] == Reports.user_id).first()
        # Check to see if the user has already rated this event
        hasRated = db.session.query(Event, Rating).filter(eventExists.event_id == Rating.event_id
                                                      ).filter(session['user_id'] == Rating.user_id).first()
        # Check to see if the user has already RSVP'd to this event
        isRSVP = db.session.query(RSVP, Event).filter(eventExists.event_id == RSVP.event_id
                                                      and session['user_id'] == RSVP.user_id).first()
        comment_form = CommentForm()
        # Increase the favortie count of an event if the favorite button is clicked
        if request.method == 'POST' and ('favorite' in request.form):
            if hasFavorited:
                flash("You cannot favorite an event more than once!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            else:
                eventExists.likes += 1
                eventFavorited = Likes(eventExists.event_id, session['user_id'])
                db.session.add(eventFavorited)
                db.session.commit()
                flash("You favorited this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
        if request.method == 'POST' and ('report' in request.form):
            if hasReported:
                flash("The event has already been reported!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            else:
                eventExists.reports += 1
                reported = Reports(eventExists.event_id, session['user_id'])
                db.session.add(reported)
                db.session.commit
                if eventExists.reports > 3:
                    eventExists = db.session.query(Event).filter_by(event_id=eventExists.event_id).one()
                    db.session.delete(eventExists)
                    db.session.commit()
                    flash("Event has been reported too many times! It is now removed.")
                    return redirect(url_for('index'))
                else:  
                    db.session.commit()
                    flash("Event Reported!")
                    return redirect(url_for('get_event', e_id=eventExists.event_id))
        # Decrease the likes if the upvote button is clicked
        if request.method == 'POST' and ('unfavorite' in request.form):
            eventExists.likes -= 1
            # Check if the user has already liked this event and if so, delete it from events they like
            if hasFavorited:
                deleteFavorited = db.session.query(Likes).filter(Likes.event_id == eventExists.event_id).filter(Likes.user_id == session['user_id']).first()
                db.session.delete(deleteFavorited)
                db.session.commit()
            else:
                flash("You haven't favortied this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            flash("You unfavorited this event!")
            return redirect(url_for('get_event', e_id=eventExists.event_id))
        if request.method == 'POST' and ('rsvp' in request.form):
            # If the user is already attending, render the current page with a dialog letting them know
            if isRSVP:
                flash("You are already attending this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            # Otherwise add the user's RSVP to the database
            else:
                attending = RSVP(eventExists.event_id, session['user_id'])
                db.session.add(attending)
                db.session.commit()
                flash("Congratulations! You have successfully RSVP'd to this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
        if request.method == 'POST' and ('un-rsvp' in request.form):
            if isRSVP:
                # Need to access the RSVP relational table since isRSVP is a Query object and delete it
                db.session.delete(isRSVP.RSVP)
                db.session.commit()
                # Send a message to the user
                flash("You have successfully un-RSVP'd from this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            else:
                # User cannot delete an RSVP if they weren't RSVP'd already
                flash("You cannot un-RSVP to an event you weren't going to!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
                
        if request.method == 'POST' and ('rating' in request.form):
            # Get rating number from rating form based on stars selected
            userRating = request.form['rating']
            # Turn rating into int
            userRating = int(userRating)
            # If the user has already rated, render the current page with updated rating
            if hasRated:
                updateRating = db.session.query(Rating).filter(Rating.event_id == eventExists.event_id).filter(Rating.user_id == session['user_id']).first()
                updateRating.ratingNum = userRating
                ratingAvg = db.session.query(func.avg(Rating.ratingNum)).\
                join(Event).\
                filter(Event.event_id == eventExists.event_id)
                db.session.commit()
                eventExists.rating = ratingAvg
                db.session.commit()
                flash("Your rating has been updated!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))
            # Otherwise add the user's rating to the database
            else:
                newRate = Rating(eventExists.event_id, session['user_id'], userRating)
                db.session.add(newRate)
                db.session.commit()
                ratingAvg = db.session.query(func.avg(Rating.ratingNum)).\
                join(Event).\
                filter(Event.event_id == eventExists.event_id)
                eventExists.rating = ratingAvg
                db.session.commit()
                flash("Congratulations! You have successfully rated this event!")
                return redirect(url_for('get_event', e_id=eventExists.event_id))

        if comment_form.validate_on_submit():
            comment_text = request.form['comment']
            new_record = Comments(eventExists.event_id, comment_text, session['user'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('get_event', e_id=eventExists.event_id))
        return render_template('EventInfo.html', user=session['user'], event=eventExists, form=comment_form)
    # If the user is logged in and tries to access an event that doesn't exist, i.e. through the URL directly
    # Redirect them to the list of all events instead
    elif session.get('user') and (not eventExists):
        return redirect(url_for('listEvents'))
    else:
        return redirect(url_for('login'))

@app.route('/events/list',methods=['GET'])
def listEvents():
    # Run a query for all events in the Event table
    events = db.session.query(Event).all()
    return render_template('EventList.html',  events=events)

'''

TAB: MY EVENTS

DESC: View events that you have created.

'''
@app.route('/events/my_events', methods=['GET', 'POST'])
def my_events():
    if session.get('user'):
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()
        return render_template('my_events.html', events=my_events, user=session['user'])
    else:
        return redirect(url_for('login'))
'''

TAB: MY EVENTS

DESC: View events that you have created.

'''
@app.route('/events/favorites')
def favorite_events():
    if session.get('user'):
        id = session.get('user_id')
        # Run a query to get all events that a user likes
        fav_events = db.session.query(Likes).filter_by(user_id=id).all()
        events = []
        # Iterate over all events that the user likes and add to a list
        for i in fav_events:
            events.append(db.session.query(Event).filter_by(event_id=i.event_id).one())
        # Only need to return the template for my_events since this will filter by liked/favorited events instead
        # of all events created by the user
        return render_template('favorite_events.html', events=events, user=session['user'])
    else:
        return redirect(url_for('login'))

'''

TAB: CREATE EVENT

DESC: Create new events tied to a user account.

'''
@app.route('/events/create', methods=['GET', 'POST'])
def new_event():
    if session.get('user'):
        eventForm = NewEventForm()
        if request.method == 'POST' and eventForm.validate_on_submit():
            name = request.form['name']
            date = request.form['date']
            desc = request.form['desc']
            user = session['user']
            user_id = session['user_id']
            
            file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
            if file.filename == '':
                file.filename = 'default.png'
                filename = 'default.png'
            else:
                filename = file.filename
                if allowed_file(filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                else:
                    # Let the user know they selected an invalid file
                    flash("Please select a valid image file (.pdf, .png, .jpg, .jpeg, .gif)")
                    return redirect(url_for('new_event'))
                
            newEvent = Event(generate_eventID(), date, name, 0.0, user, 0, desc, 0, user_id, filename)
            db.session.add(newEvent)
            db.session.commit()
            # Redirect the user to the newly created event's page
            return redirect(url_for('get_event', e_id=newEvent.event_id))
        else:
            # Display new_event view if something goes wrong
            return render_template('new_event.html', form=eventForm, user=session['user'])
    else:
        # Have the user login before creating an event
        return redirect(url_for('login'))

'''

TAB: DELETE

DESC: Deletes the event in question. Currently redirects to home page.
'''
@app.route ('/events/delete/<event_id>', methods = ['POST'])
def delete_event(event_id):
    #check if a user is saved in session
    if session.get('user'):

        #retrieve event from database
        my_event = db.session.query(Event).filter_by(event_id=event_id).one()
        db.session.delete(my_event)
        db.session.commit()

        return redirect (url_for('my_events'))
    else:
        #user is not in session redirect to login
        return redirect(url_for('login'))
@app.route ('/events/edit/<event_id>', methods = ['POST', 'GET'])
def edit_event(event_id):
    if session.get('user'):
        editForm = NewEventForm()
        event = db.session.query(Event).filter_by(event_id=event_id).first()
        if editForm.validate_on_submit():
            new_name = request.form['name']
            new_date = request.form['date']
            new_desc = request.form['desc']
            user = session['user']
            user_id = session['user_id']

            file = request.files['file']

            if file.filename == '':
                file.filename = 'default.png'
                filename = 'default.png'
            else:
                filename = file.filename
                if allowed_file(filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                else:
                    # Let the user know they selected an invalid file
                    flash("Please select a valid image file (.pdf, .png, .jpg, .jpeg, .gif)")
                    return redirect(url_for('edit_event', event_id=event.event_id))

            event = db.session.query(Event).filter_by(event_id=event_id).first()
            event.name = new_name
            event.date = new_date
            event.desc = new_desc
            event.filename = filename
            db.session.commit()
            return redirect(url_for('get_event', e_id=event.event_id))
        else:
            return render_template('edit_event.html', form=editForm, user=session['user'])
    else:
        return redirect(url_for('login'))


'''

TAB: REGISTER

DESC: Only active when a user logged out. Register a new user to the database.

'''
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        email = request.form['email']
        # create user model
        newUser = User(generate_userID(), email, firstName, lastName, h_password)
        # add user to database and commit
        db.session.add(newUser)
        db.session.commit()
        # save the user's name to the session
        session['user'] = firstName
        session['user_id'] = newUser.user_id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('index', user=session['user']))

    # something went wrong - display register view
    return render_template('Registration.html', form=form)

'''

TAB: LOGOUT

DESC: Only active when a user is logged in. The place where the user wishes to log out.

'''
@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))

'''

TAB: SIGN IN

DESC: Only active when a user is logged out. The place where the user enters existing account information to login.

'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.user_id
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

'''

DESC: Function to randomly generate user IDs.

'''
def generate_userID():
    #Generate 4 digit number for userID and ensure that all users have unique IDs
    id = randint(1000, 9999)
    idTaken = User.query.filter_by(user_id=id).first()
    while idTaken:
        id = randint(1000, 9999)
        idTaken = User.query.filter_by(user_id=id).first()
    return id

'''

DESC: Function to randomly generate event IDs.

'''
def generate_eventID():
    #Generate 6 digit number for eventID and ensure that all events have unique IDs
    id = randint(100000, 999999)
    idTaken = Event.query.filter_by(event_id=id).first()
    while idTaken:
        id = randint(100000, 999999)
        idTaken = Event.query.filter_by(event_id=id).first()
    return id


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
