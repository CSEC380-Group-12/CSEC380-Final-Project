# Flask imports
from queue import Queue

import flask
from flask import Flask, render_template, redirect, url_for, request, abort, session, send_from_directory, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
from common import *  # database creds
import pymysql  # for the MariDB container
import sys
import os
import datetime
import subprocess
import time
# hashing and encrypting
import hashlib
import secrets
from werkzeug.utils import secure_filename
from threading import Thread
import urllib.parse as urlparse
import requests

# wait for database container to load before flask
def database_checker():
    while True:
        try:
            conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
            with conn.cursor() as cursor:
                query = f"SELECT userID FROM accounts WHERE username = 'brendy';"
                cursor.execute(query)
                conn.commit()
                uid = cursor.fetchone()[0]
                conn.close()
                if int(uid) == 3:
                    print("[*] Done!")
                    return
        except:
            print("[*] Waiting for database ...", flush=True)
            time.sleep(10)
            continue

q = Queue()
t = Thread(target=database_checker)
t.start()
q.join()
q.put(None)
t.join()
##### Database loaded ....

# flask init
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_url_path='/static', template_folder='templates')


# flask session init
app.secret_key = secrets.token_bytes(64)

# rate limit for password brute force
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["28000 per day", "1000 per hour", "20 per minute"]
)

# configure CORS
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

# Upload variables
UPLOAD_DIR = f'/webapp/static/uploads'
# TODO: exploit this ? makedir -> and call back ?
cmd=f"mkdir -p {UPLOAD_DIR}"
output = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE).communicate()[0]

CREATE_TEST_USER = True

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv', 'm4v'}
app.config['UPLOAD_DIR'] = UPLOAD_DIR
# file upload limit = 200mb
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024


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
    testuser1 = 'admin'
    password = 'admin'
    hash_object = hashlib.md5(password.encode())
    test_hash = hash_object.hexdigest()

    query = f"SELECT userID, pass_hash FROM accounts WHERE username = '{testuser1}'"
    conn.commit()
    cursor.execute(query)
    cursor.execute(f"INSERT INTO accounts(username, pass_hash) VALUES ('{testuser1}', '{test_hash}')")
    print(f"added test user: {testuser1}")
    cursor.close()
    conn.commit()
    conn.close()

    global CREATE_TEST_USER
    CREATE_TEST_USER = False



def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_videos():
#     conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
#     try:
#         with conn.cursor() as cursor:
#             # Read a single record
#             sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#             cursor.execute(sql, ('webmaster@python.org',))
#             result = cursor.fetchone()
#             print(result)
#     finally:
#         conn.close()


def file_check(filename):
    return os.path.isfile(os.path.join(app.config['UPLOAD_DIR'], filename))

def download_form_url(url, title, filename):
    # parts = urlparse(url)
    try:
        if allowed_files(filename):
            r = requests.get(url)
            if r.status_code() == 200:
                vid_path = os.path.join(app.config['UPLOAD_DIR'], filename)
                with open(vid_path, 'wb') as fp:
                    fp.write(r.content)
    except Exception:
        flash("Failed to download file")
    try:
        # add video metadata to the database
        conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
        cursor = conn.cursor()
        userID = session['uid']
        query = f"INSERT INTO videos(userID, videoTitle, fileName) VALUES ('{userID}', '{title}', '{filename}')"
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        return filename

    except Exception as e:
        print(e, flush=True)
        return None



def process_file_upload():
    # if its a url
    # TODO: exploit ? https://gist.github.com/fedir/5883651
    url = request.form.get('file.URL', '')
    parts = urlparse.urlsplit(url)
    title = request.form.get('vidTitle', '')
    if parts.scheme in {'http', 'https'}:
        return download_form_url(url, title, parts.path[1:])

    # check if the post request contains a file
    if 'file' not in request.files:
        print('no file selected', flush=True)
        return None

    fp = request.files['file']
    # check file name length
    if fp.filename == '' or title == '':
            print(f'no file name\nfp.fileName{fp.filename}, title: {title}', flush=True)
            return None
    filename = secure_filename(fp.filename)  # generate a secure name
    if fp and allowed_files(fp.filename):
        try:
            # add video metadata to the database
            conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
            cursor = conn.cursor()
            userID = session['uid']
            query = f"INSERT INTO videos(userID, videoTitle, fileName) VALUES ('{userID}', '{title}', '{filename}')"
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            # save the video
            fp.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            return filename

        except Exception as e:
            print(e, flush=True)
            return None
    return None




@app.route('/')
def route_index():  
    # app_name = os.getenv("APP_NAME")  
    if is_session_logged_in():
        conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
        video_list = []
        try:
            with conn.cursor() as cursor:
                query = "SELECT videoURL, videoTitle, userID FROM videos"
                cursor.execute(query)
                result = cursor.fetchone()
                while result is not None:
                    video_list.append(result)
                    result = cursor.fetchone()
                cursor.close()
        except Exception as e:
            print(e, flush=True)
        finally:
            conn.close()
        final_list = []
        for i in video_list:
            j = i.split()
            for x in j:
                final_list.append(x)
        print(video_list)
        return render_template('home.html', my_list=final_list)
    else:
        return render_template('login.html')


@app.route('/returnToBrowse', methods=['GET', 'POST'])
def route_return():
    if is_session_logged_in():
        return redirect('/')
    else:
        return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("14400/day;600/hour;10/minute")
def route_login():
    if request.method == 'GET':
        return redirect('/')

    username = request.form['username']
    password = request.form['password']
    if username == "admin2" and CREATE_TEST_USER:
        create_test_users()
        return redirect("/login")

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

@app.route('/logout', methods=['GET', 'POST'])
def route_logout():
    if is_session_logged_in():
        if process_logout_request():
            return redirect('/')
    
    redirect('/login')

# route to play videos
@app.route('/uploads/<filename>')
def route_uploaded_file(filename):
    if not is_session_logged_in():
        return redirect('/login')

    return send_from_directory(app.config['UPLOAD_DIR'], filename)

@app.route('/upload', methods=['GET'])
def route_upload():
    if is_session_logged_in():
        return render_template('upload.html')
    else:
        return render_template('login.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if is_session_logged_in():
        filename = process_file_upload()
        if filename is not None:
            vid_url = url_for('static', filename=f"uploads/{filename}")
            flash("Video uploaded successfully")
            flash("Redirecting to Video..")
            
            flash("url for video:")
            flash(f"http://0.0.0.0{vid_url}")
            # return redirect(vid_url)
        else:
            flash(u"Video failed to upload", 'error')
            # return redirect('/uploadFail')
    else:
        return redirect('/login')
    return redirect('/upload')


# serving of the uploaded files
# redirect the user to /uploads/filename
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIR'],
                               filename)


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


@app.route('/delete', methods=['GET', 'POST'])
def route_delete():
    if is_session_logged_in():
        return render_template('delete.html')
    else:
        return render_template('login.html')


@app.route('/DeleteCSS.css')
def route_DeleteCSS():
    return app.send_static_file('CSS/DeleteCSS.css')


@app.route('/LoginCSS.css')
def route_LoginCSS():
    return app.send_static_file('CSS/LoginCSS.css')


@app.route('/LandingCSS.css')
def route_LandingCSS():
    return app.send_static_file('CSS/LandingCSS.css')


@app.route('/UploadCSS.css')
def route_UploadCSS():
    return app.send_static_file('CSS/UploadCSS.css')



# vim:tabstop=4
# vim:shiftwidth=4

