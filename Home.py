import os  # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
import re
from database import db
from models import User as User
from models import Event as Event

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

logDetails = {'LoggedIn': False, 'User': None}
errorDetails = {'HasError': False, 'Message': None}


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    if logDetails['LoggedIn']:
        return render_template('Home.html', user=logDetails.get('User'))
    else:
        return render_template('Home.html', user=None)
@app.route('/events/<e_id>')
def get_event(e_id):
    event = Event.query().filter_by(event_id=e_id).one()
    user = "Test User"
    return render_template('EventInfo.html',user=user,event=event)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        userEmail = request.form['user_email']
        name = request.form['full_name']
        password = request.form['user_password']
        validation = validate_credentials(userEmail, name, password)
        if validation.get('HasError'):
            return render_template('Registration.html', error = errorDetails)
        newUser = User(userEmail, name, password)
        db.session.add(newUser)
        db.session.commit()
        currentUser = User.query.filter_by(email=userEmail).one()
        logDetails['User'] = currentUser
        logDetails['LoggedIn'] = True
        return redirect(url_for('index', user=currentUser))
    else:
        return render_template('Registration.html', error = errorDetails)

def validate_credentials(e, n, p):
    if str(e) == "" or str(n) == "" or str(p) == "":
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
        errorDetails['Message'] = ""
        return errorDetails


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
