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

# A class to represent a Video
class Video:
	vidID = int()
	userID = int()
	videoTitle = str()
	filename = str()

	def __init__(self, vidID, userID, videoTitle, filename):
		self.vidID = vidID
		self.userID = userID
		self.videoTitle = videoTitle
		self.filename = filename

	# Returns the path for this video
	def getPath():
		return file_check(filename)

def get_username_from_id(uid):
	# TODO
	pass

# a helper function that queries the database and returns the resualt
def query_database(query, fetchall=False):
    # print(f"query: {query}")
    # print(f"fetchall: {fetchall}")
    result = None
    conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            if fetchall:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            return result
        conn.commit()
    except Exception as e:
        print(f"Error: {e}", flush=True)
    finally:
        conn.close()

# wait for database container to load before flask
def database_checker():
    while True:
        try:
            query = f"SELECT userID FROM accounts WHERE username = 'brendy';"
            result = query_database(query)
            # print(f"result: {result}", flush=True)
            uid = result[0]
            # print(f"uid: {uid}", flush=True)
            if int(uid) == 3:
                print("[*] Database loaded!")
                return
            # conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
            # with conn.cursor() as cursor:
            #     query = f"SELECT userID FROM accounts WHERE username = 'brendy';"
            #     cursor.execute(query)
            #     conn.commit()
            #     uid = cursor.fetchone()[0]
            #     conn.close()
            #     if int(uid) == 3:
            #         print("[*] Done!")
            #         return
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
        # conn = pymysql.connect(db_host, db_user, db_passwd, db_database, charset='utf8mb4')
        # cursor = conn.cursor()
        hash_object = hashlib.md5(password.encode())
        cur_hash = hash_object.hexdigest()
        # Retrieve user data (uid, password_hash)
        query = f"SELECT userID, pass_hash FROM accounts WHERE username = '{username}'"
        result = query_database(query, True)
        print(f"[!] result: {result}", flush=True)
        # cursor.execute(query, data)
        for (userID, password_hash) in result:
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

# # creates the user admin:admin
# def create_test_users():
#     # Add a test user
#     conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
#     cursor = conn.cursor()
#     testuser1 = 'admin'
#     password = 'admin'
#     hash_object = hashlib.md5(password.encode())
#     test_hash = hash_object.hexdigest()

#     query = f"SELECT userID, pass_hash FROM accounts WHERE username = '{testuser1}'"
#     conn.commit()
#     cursor.execute(query)
#     cursor.execute(f"INSERT INTO accounts(username, pass_hash) VALUES ('{testuser1}', '{test_hash}')")
#     print(f"added test user: {testuser1}")
#     cursor.close()
#     conn.commit()
#     conn.close()
# ## Create the user admin:admin
# create_test_users()

# allowed extentions
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: retrive videos
# def get_videos():
#     conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
#     try:
#         with conn.cursor() as cursor:
#             # Read a single record
#             sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#             cursor.execute(sql, ('webmaster@python.org',))
#             result = cursor.fetchone()
#             print(resultFone)        # conn = pymysql.connect(db_host, db_user, db_passwd, db_database, charset='utf8mb4')
        # cursor = conn.cursor()

#     finally:
#         conn.close()

# check if a file exists (TODO: not used yet)
def file_check(filename):
    return os.path.isfile(os.path.join(app.config['UPLOAD_DIR'], filename))

# download a video form a given url
def download_form_url(url, title, filename):
    downloaded = False
    if not allowed_files(filename):
        return None
    
    r = requests.get(url, stream=True)
    path = os.path.join(app.config['UPLOAD_DIR'], filename)
    print(f"Got the request {r}", flush=True)
    print(f"R status code: {r.status_code}", flush=True)
    print(f"path to save the file: {path}", flush=True)
    try:
        if r.status_code == 200:
            with open(path, "wb") as fp:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        fp.write(chunk)
            downloaded = True
        else:
            flash(f"Video url return with status code {r.status_code()}", 'error')
    except Exception as e:
        flash("Failed to download file", 'error')
        flash(f"error: {e}", 'error')
    if not downloaded:
        return None
    try:
        # add video metadata to the database
        # conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
        # cursor = conn.cursor()
        userID = session['uid']
        query = f"INSERT INTO videos(userID, videoTitle, fileName) VALUES ('{userID}', '{title}', '{filename}')"

        query_database(query)
        # cursor.execute(query)
        # cursor.close()
        # conn.commit()
        # conn.close()

        return filename

    except Exception as e:
        return None

# processes a file upload request. 
def process_file_upload():
    # if its a url
    # TODO: exploit ? https://gist.github.com/fedir/5883651
    url = request.form.get('file.URL', '')
    parts = urlparse.urlsplit(url)
    title = request.form.get('vidTitle', '')
    if parts.scheme in {'http', 'https'}:
        filename = parts.path.split('/')[-1]
        return download_form_url(url, title, filename)

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
            # conn = pymysql.connect(db_host, db_user, db_passwd, db_database)
            # cursor = conn.cursor()
            userID = session['uid']
            query = f"INSERT INTO videos(userID, videoTitle, fileName) VALUES ('{userID}', '{title}', '{filename}')"

            query_database(query)
            # cursor.execute(query)
            # cursor.close()
            # conn.commit()
            # conn.close()

            # save the video
            fp.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            return filename

        except Exception as e:
            print(e, flush=True)
            return None
    return None

def delete_video(filename):
    pass
    

@app.route('/')
def route_index():  
    if is_session_logged_in():
        query = "SELECT * FROM accounts"
        videos = query_database(query, fetchall=True)
        final_list = [videos]
        #if videos is not None:
            #for i in videos:     #Splits up the requested data into individual components
                #final_list.append(str(i[0]))
                #final_list.append(str(i[1]))
                #final_list.append(str(i[2]))
        example = ["Jinja works!", str(len(videos))]
        return render_template('home.html', my_list=final_list, test_list=example)
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


def get_video(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


# route to play videos
@app.route('/videoPlayer/<filename>')
def route_video_player(filename):
    if not is_session_logged_in():
        return redirect('/login')

    vid = get_video(filename)

    return render_template('videoPlayer.html', username=session.get('username'))
    # return send_from_directory(app.config['UPLOAD_DIR'], filename)



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
            #TODO: change 
            flash(f"http://0.0.0.0/static/uploads/{filename}")
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

