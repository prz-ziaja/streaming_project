import re

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from prometheus_flask_exporter import PrometheusMetrics

from pager import Pager
import os
import pymongo
import sys
import yaml
import logging
import pickle
from PIL import Image as im
import json
import threading
import time

# Make connection to MongoDB with photo data
with open("api_config.yaml") as yaml_file:
    config_dict = yaml.load(yaml_file)["config_dictionary"]

db = pymongo.MongoClient(
    'mongo1:27017',
    username=config_dict['mongo_user'],
    password=config_dict['mongo_password'],
    authSource=config_dict['mongo_database'],
    authMechanism='SCRAM-SHA-256')[config_dict['mongo_database']]
try:
    db.list_collections()
except Exception as e:
    logging.error(f"Problem with connection to MongoDB\n{e.args}")
    sys.exit(2)

collection_photos = db[config_dict['collection_photos']]
collection_labels = db[config_dict['collection_labels']]

user_history = {}

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'mysql-db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'users'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
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
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
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


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST
# requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/find_by_tag/<index>')
def browser(index):
    # We need user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    user = account['username']
    index = int(index)
    photo_date = user_history[user][index]
    return render_template("browser.html", data=photo_date[0], all_info=photo_date[1],
                           next_pic=f"{(index + 1) % len(user_history[user])}",
                           previous_pic=f"{(index - 1) % len(user_history[user])}")


def get_info(founded, text):
    # TODO wybiera tylko jednen pasujacy element ze zdj
    # catched - wszystkie obiekty na zdj
    catched = founded["labels"]
    info = []
    for i in catched:
        # i[:4] tagi zaczynaja sie od 5 elementu
        if text in i[4:]:
            info.append(i)
    return info


def get_photos(text, found, user):
    text_data = {}
    for i in found[:20]:
        photo = pickle.loads(collection_photos.find_one({"id": i['id']})['photo'])
        photo = im.fromarray(photo)
        b, g, r = photo.split()
        photo = im.merge("RGB", (r, g, b))
        photo.save(f'static/images/{i["id"]}.png')
        # user_history[user].append(i["id"])
        info = get_info(i, text)
        user_history[user].append([i["id"], info])


@app.route('/goto', methods=['POST', 'GET'])
def goto():
    # We need user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    user = account['username']

    user_history[user] = []
    text = request.form['index']

    labels = [x.strip() for x in text.split(',')]
    found = [*collection_labels.find({'labels': {"$elemMatch": {"$elemMatch": {"$in": labels}}}})]

    t = threading.Thread(target=get_photos, args=(text, found, user,))
    t.start()
    time.sleep(2)
    return redirect('/pythonlogin/find_by_tag/0')


if __name__ == '__main__':
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    app.run(host=hostname, port=80)
