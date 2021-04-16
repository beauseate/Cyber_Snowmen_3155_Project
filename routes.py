import os  # os is used to get environment variables IP & PORT

import bcrypt
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
import re
from database import db
from models import User as User
from models import Event as Event
from random import randint
from flask import session
from forms import RegisterForm, LoginForm, NewEventForm

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
db.init_app(app)
with app.app_context():
    db.create_all()

logDetails = {'LoggedIn': False, 'User': None}
errorDetails = {'HasError': False, 'Message': None}

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #commenting out since this hasn't been implemented yet. works without it.
    # if request.method == 'POST':
    #     searchEvent = request.form['event']
    #     eventExists = Event.query.filter_by(name=searchEvent).first()
    #     if eventExists:
    #         eventID = eventExists.event_id
    #         return redirect(url_for('get_event', e_id=eventID))
    if session.get('user'):
        return render_template('Home.html', user=session['user'])
    else:
        return render_template('Home.html')


@app.route('/events/<e_id>', methods = ['GET', 'POST'])
def get_event(e_id):
    eventExists = db.session.query(Event).filter_by(event_id=e_id).first()
    if session.get('user') and eventExists:
        if request.method == 'POST':
            eventExists.likes += 1
            db.session.commit()
            #Redirecting to homepage is a placeholder for now
            return redirect(url_for('index'))
        return render_template('EventInfo.html', user=session['user'], event=eventExists)
    else:
        #Only a placeholder until a login screen is added
        return redirect(url_for('index'))


@app.route('/events/create', methods=['GET', 'POST'])
def new_event():
    if session.get('user'):
        eventForm = NewEventForm()
        if request.method == 'POST' and eventForm.validate_on_submit():
            name = request.form['Event_Name']
            day = request.form['Date'].strftime('%d')
            month = request.form['Date'].strftime('%m')
            year = request.form['Date'].strftime('%Y')
            desc = request.form['Description']
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            dateList = [month, day, year]
            date = "/"
            date = date.join(dateList)
            user = session['user']
            newEvent = Event(generate_eventID(), date, name, 0.0, user, 0, desc )
            db.session.add(newEvent)
            db.session.commit()
            return redirect(url_for('get_event', e_id = newEvent.event_id))
        else:
            return render_template('new_event.html')
    else:
        #Placeholder until login screen is added
        return redirect(url_for('index'))


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
    OLD Registration

    if request.method == 'POST':
        userEmail = request.form['user_email']
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        password = request.form['user_password']
        validation = validate_credentials(userEmail, firstName, lastName, password)
        if validation.get('HasError'):
            return render_template('Registration.html', error=errorDetails)
        h_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        newUser = User(generate_userID(), userEmail, firstName, lastName, h_password)
        db.session.add(newUser)
        db.session.commit()
        session['user'] = firstName
        session['user_id'] = newUser.user_id
        return redirect(url_for('index', user=session['user']))
    else:
        #errorDetails['HasError'] = False
        return render_template('Registration.html')
        '''


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))


##login goes here
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






#could probably get rid of this in the future:
#i believe we have built in validation with WTForms
def validate_credentials(e, fn, ln, p):
    if str(e) == "" or str(fn) == "" or str(ln) == "" or str(p) == "":
        errorDetails['HasError'] = True
        errorDetails['Message'] = 'Fields cannot be left empty.'
        return errorDetails
    if not User.query.filter_by(email=e).first() is None:
        errorDetails['HasError'] = True
        errorDetails['Message'] = 'Email already in use.'
        return errorDetails
    if re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', e) is None:
        errorDetails['HasError'] = True
        errorDetails['Message'] = 'Invalid email'
        return errorDetails
    if re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', p) is None:
        errorDetails['HasError'] = True
        errorDetails['Message'] = '''
                                    Password must contain
                                                   * At least one number,
                                                   * At least one uppercase letter and one lowercase letter,
                                                   * At least one special symbol,
                                                   * Have a length between 6-20 characters
                         '''

        return errorDetails
    else:
        errorDetails['HasError'] = False
        return errorDetails


def generate_userID():
    #Generate 4 digit number for userID and ensure that all users have unique IDs
    id = randint(1000, 9999)
    idTaken = User.query.filter_by(user_id=id).first()
    while idTaken:
        id = randint(1000, 9999)
        idTaken = User.query.filter_by(user_id=id).first()
    return id

def generate_eventID():
    #Generate 6 digit number for eventID and ensure that all events have unique IDs
    id = randint(100000, 999999)
    idTaken = Event.query.filter_by(event_id=id).first()
    while idTaken:
        id = randint(100000, 999999)
        idTaken = Event.query.filter_by(event_id=id).first()
    return id

#could probably get rid of this in the future:
#i believe we have built in validation with WTForms
def validate_input(name, day, month, year, desc):
    if name == "" or day == "" or month == "" or year == "" or desc == "":
        errorDetails['HasError'] = True
        errorDetails['Message'] = 'Fields cannot be left blank'
        return errorDetails
    try:
        month = int(month)
        day = int(day)
        year = int(year)
    except ValueError:
        errorDetails['HasError'] = True
        errorDetails['Message'] = 'Date fields must be numerical'
        return errorDetails
    if month < 1 or month > 12:
        errorDetails['HasError' ]= True
        errorDetails['Message'] = 'Month has to be between 01 and 12'
        return errorDetails
    if year < 2021 or (year == 2021 and month < 4):
        errorDetails['HasError' ]= True
        errorDetails['Message'] = 'It has to be an event in the future!'
        return errorDetails
    if day < 0 or day > 31:
        errorDetails['HasError' ]= True
        errorDetails['Message'] = 'Day must be between 0 and 31'
        return errorDetails
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        if day > 29:
            errorDetails['HasError' ] = True
            errorDetails['Message'] = 'Day cannot be greater than 29'
            return errorDetails
        else:
            if day > 28:
                errorDetails['HasError' ] = True
                errorDetails['Message'] = 'Day cannot be greater than 28'
                return errorDetails
    if month == 4 or month == 6 or month == 9 or month == 11:
        if day > 30:
            errorDetails['HasError' ] = True
            errorDetails['Message'] = 'Day cannot be greater than 30'
            return errorDetails
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31 :
            errorDetails['HasError' ]= True
            errorDetails['Message'] = 'Day cannot be greater than 31'
            return errorDetails

    errorDetails['HasError'] = False
    errorDetails['Message'] = ""
    return errorDetails






if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
