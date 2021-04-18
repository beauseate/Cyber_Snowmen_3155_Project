import os  # os is used to get environment variables IP & PORT

import bcrypt
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import User as User, Likes
from models import Event as Event
from random import randint
from flask import session
from forms import RegisterForm, LoginForm, NewEventForm
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
Images = join(dirname(realpath(__file__)),'Images')
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
        events = Event.query.filter(Event.name.ilike(f'%{searchEvent}%'))
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
        hasLiked = db.session.query(Likes).filter_by(event_id=eventExists.event_id).first()
        # Increase the likes of an event if the upvote button is clicked
        if request.method == 'POST' and ('upvote' in request.form):
            if hasLiked:
                return render_template('EventInfo.html', user=session['user'], event=eventExists, hasLiked=hasLiked)
            eventExists.likes += 1
            eventLiked = Likes(generate_likeID(), eventExists.event_id, session['user_id'])
            db.session.add(eventLiked)
            db.session.commit()
            return redirect(url_for('get_event', e_id=eventExists.event_id))
        # Decrease the likes if the upvote button is clicked
        if request.method == 'POST' and ('downvote' in request.form):
            eventExists.likes -= 1
            # Check if the user has already liked this event and if so, delete it from events they like
            if hasLiked:
                db.session.delete(hasLiked)
                db.session.commit()
            return redirect(url_for('get_event', e_id=eventExists.event_id))
        return render_template('EventInfo.html', user=session['user'], event=eventExists)
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
        return render_template('my_events.html', events=my_events, user =session['user'])
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
            
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
            if file.filename == '':
                    
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename =file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                
            newEvent = Event(generate_eventID(), date, name, 0.0, user, 0, desc, 0, user_id,filename)
            db.session.add(newEvent)
            db.session.commit()
            # Redirect the user to the newly created event's page
            return redirect(url_for('get_event', e_id=newEvent.event_id))
        else:
            # Display new_event view if something goes wrong
            return render_template('new_event.html', form=eventForm)
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
    event = db.session.query(Event).filter_by(event_id=event_id).first()
    if session.get('user') and request.method == 'POST':
        editForm = NewEventForm()
        if request.method == 'POST' and editForm.validate_on_submit():
            new_name = request.form['name']
            new_date = request.form['date']
            new_desc = request.form['desc']
            user = session['user']
            user_id = session['user_id']

            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            event.name = new_name
            event.date = new_date
            event.desc = new_desc
            event.filename = filename
            db.session.commit()
            return redirect(url_for('get_event', e_id=event.event_id))
        else:
            return render_template('edit_event.html', form=editForm)
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
'''

DESC: Function to randomly generate Like IDs.

'''
def generate_likeID():
    # Arbitrary because the Likes table needs a primary key
    # Generate 5 digit number for likeID and ensure that all Likes have unique IDs
    id = randint(100, 999)
    idTaken = Likes.query.filter_by(likes_id=id).first()
    while idTaken:
        id = randint(100, 999)
        idTaken = Likes.query.filter_by(likes_id=id).first()
    return id


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
