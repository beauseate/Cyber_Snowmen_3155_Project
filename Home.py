# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
import re

app = Flask(__name__)     # create an app
a_user = {'name': 'Test_User', 'email':'Test_User@uncc.edu', 'password' : None}

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    return render_template('Home.html', user = a_user)

@app.route('/register', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['user_email']
        name = request.form['f_name']
        password = request.form['user_password']
        if not re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email):
            return '<h1> Invalid email </h1>'
        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password):
            return ''' <h1>
                            Error! <br>
                            Password must contain: <br>
                                    At least one number <br>
                                    At least one uppercase letter and one lowercase letter <br>
                                    At least one special symbol <br>
                                    Have a length between 6-20 characters
                                    </h1>
                        '''
        if str(email) == "" or str(name) == "":
            return '<h1> Fields cannot be left empty.'
        a_user['name'] = request.form['f_name']
        a_user['email'] = request.form['user_email']
        a_user['password'] = request.form['user_password']
        return redirect(url_for('index'))
    else:
        return render_template('Registration.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.