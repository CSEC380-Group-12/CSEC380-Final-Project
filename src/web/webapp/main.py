# imports
import flask
from flask import Flask, render_template, redirect, url_for, request, abort, session, send_from_directory, flash
from common import *
import pymysql
import sys
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
import hashlib
from common import *
import secrets
from werkzeug.utils import secure_filename

# flask init
CREATE_TEST_USER = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_url_path='/static', template_folder='templates')

# flask session init
app.secret_key = secrets.token_bytes(64)
app.config['SESSION_TYPE'] = 'filesystem'

# rate limit for password brute force
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["28000 per day", "1000 per hour", "20 per minute"]
)

# configure CORS
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


# Checks if the current session is logged in.
# @return			True if the current session is logged in, otherwise False.
def is_session_logged_in():
    return 'uid' in session


# Processes a login request.
# @param username	The username for the login request.
# @param password	The password for the login request.
# @return			True if the login is successful/valid, otherwise False.
def process_login_request(username, password):
    conn = None
    cursor = None
    try:
        # Connect to the Database
        conn = pymysql.connect(db_host, db_user, db_passwd, db_database, charset='utf8mb4')
        cursor = conn.cursor()
        hash_object = hashlib.md5(password.encode())
        cur_hash = hash_object.hexdigest()
        # Retrieve user data (uid, password_hash)
        query = '''SELECT userID, pass_hash FROM accounts WHERE username = (%s)'''
        data = (username,)
        cursor.execute(query, data)
        for (userID, password_hash) in cursor:
            # validate password hash
            if password_hash == cur_hash:
                session['username'] = username
                session['uid'] = userID
                return True
            return False
    except Exception as e:
        # Some error occurred, so fail the login
        print('Login Error: exception error (user ' + username + ')', file=sys.stderr)
        return False
    finally:
        if conn is not None:
            conn.close()
        if cursor is not None:
            cursor.close()


# Processes a logout request.
# @return			True if the logout was successful, otherwise False.
def process_logout_request():
    if 'uid' not in session:
        return False
    # TODO - Implement Logout Here
    session.pop('uid', None)
    flash('You were logged out.')
    return True

def create_test_users():
    # Add a test user

    conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
    cursor = conn.cursor()
    testuser1 = 'admin2'
    password = 'admin2'
    hash_object = hashlib.md5(password.encode())
    test_hash = hash_object.hexdigest()

    query = '''SELECT userID, pass_hash FROM accounts WHERE username = (%s)'''
    data = (testuser1,)
    cursor.execute(query, data)
    print("here", file=sys.stderr)
    for (userID, password_hash) in cursor:
        if password_hash == test_hash:
            return
        else:
            cursor.execute(f"INSERT INTO accounts(username, pass_hash) VALUES ('{testuser1}', '{test_hash}')")

    cursor.close()
    conn.commit()
    conn.close()


@app.route('/')
def route_index():
    if is_session_logged_in():
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("14400/day;600/hour;10/minute")
def route_login():
    if CREATE_TEST_USER:
        create_test_users()

    if request.method == 'GET':
        return redirect('http://localhost:5000')

    username = request.form['username']
    password = request.form['password']
    if process_login_request(username, password) is True:
        return redirect('/')
    else:
        return redirect('/invalid_login')


@app.route('/invalid_login')
def route_invalid_login():
    if is_session_logged_in():
        redirect('/')
    else:
        return render_template('login-fail.html')


@app.route('/upload', methods=['GET'])
def route_upload():
    if is_session_logged_in():
        return render_template('upload.html')
    else:
        return render_template('login.html')


def allowed_files(filename):
    allowed_extensions = {'mp4', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post if the post request contains a file
        if 'file' not in request.files:
            flash('no file selected')
            return redirect("/uploadFail")
        file = request.files['file']
        if len(file.filename) < 1:
            flash("No file selected")
            return redirect("/uploadFail")
            
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            # TODO: save file to db
            flash('File successfully uploaded')
            return redirect('/uploadSuccess')
        else:
            return redirect('/uploadFail')
    else:
        return render_template("/upload")

@app.route('/uploadSuccess', methods=['POST', 'GET'])
def route_upload_success():
    if is_session_logged_in():
        return render_template("uploadSuccess.html")
    else:
        return redirect("/login")


@app.route('/uploadFail', methods=['POST', 'GET'])
def route_upload_fail():
    if is_session_logged_in():
        return render_template("uploadFail.html")
    else:
        return redirect("/login")


@app.route('/logout', methods=['GET', 'POST'])
def route_logout():
    if process_logout_request() == True:
        return redirect('/')
    else:
        abort(405)


@app.route('/returnToBrowse', methods=['GET', 'POST'])
def route_return():
    if is_session_logged_in():
        return redirect('/')
    else:
        return redirect("/login")


@app.route('/delete', methods=['GET', 'POST'])
def route_delete():
    if is_session_logged_in():
        return render_template('delete.html')
    else:
        return render_template('login.html')


@app.route('/DeleteCSS.css')
def route_DeleteCSS():
    return app.send_static_file('DeleteCSS.css')


@app.route('/LoginCSS.css')
def route_LoginCSS():
    return app.send_static_file('LoginCSS.css')


@app.route('/LandingCSS.css')
def route_LandingCSS():
    return app.send_static_file('LandingCSS.css')


@app.route('/UploadCSS.css')
def route_UploadCSS():
    return app.send_static_file('UploadCSS.css')

# vim:tabstop=4
# vim:shiftwidth=4