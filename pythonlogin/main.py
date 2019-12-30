from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb.cursors
import re
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)
    # http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
   # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'GET':
        return render_template("register.html")

    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        return render_template('index.html', msg=msg)
    # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home', methods=['GET','POST'])
def home():
    # Check if user is loggedin
    if request.method == 'GET':
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    else:
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))
    # To get the info from the tables
        Name = request.form['Name']
        Dob = request.form['Dob']
        Gender = request.form['Gender']
        Offile_Location = request.form['Office_Location']
        Office_Email_ID = request.form['Office_Email_ID']
        Office_Mobile_Number = request.form['Office_Mobile_Number']
        Employer_with_Experience = request.form['Employer_with_Experience']
        Previous_Employer1_Experience = request.form['Previous_Employer1_Experience']
        Previous_Employer2_Experience = request.form['Previous_Employer2_Experience']
        Soft_Skills = request.form['Soft Skills']
        Certifications = request.form['Certifications']
        Projects_Worked = request.form['Projects Worked']
        Hobbies = request.form['Hobbies']
        Personal_Mobile_No = request.form['Personal Mobile No']
        Permanent_Address = request.form['Permanent Address']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (Name, Dob, Gender, Offile_Location, Office_Email_ID, Office_Mobile_Number, Employer_with_Experience, Previous_Employer1_Experience, Previous_Employer2_Experience, Soft_Skills, Certifications, Projects_Worked, Hobbies, Personal_Mobile_No, Permanent_Address))
        mysql.connection.commit()
        return render_template('home.html')
    # http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        cursor.execute("SELECT * FROM info")
        info = cursor.fetchall()
        # Show the profile page with account info
        return render_template('profile.html', account=account , info=info)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
if __name__ == '__main__':
   app.run()