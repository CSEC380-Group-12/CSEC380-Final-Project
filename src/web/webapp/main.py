from flask import *
from config import *
import pymysql
import base64
import datetime
from os.path import isfile, join
from mimetypes import MimeTypes
from os import listdir
from wand.image import Image
import wand.image
import hashlib
import json
import time
import hmac
import copy
import sys
import os

import wand.image

app = Flask(__name__)
app.secret_key = 'Make sure to change this to a really long, super secure password when testing is done!'

# Session variables:
# uid				int: The UID of the user that is logged in

# Connect to the Database
def db_conn():
	sql_conn = mysql.connector.connect(
		host=db_host,
		user=db_user,
		passwd=db_passwd,
		database=db_database
	)
	return sql_conn

# Checks if the current session is logged in.
# @return			True if the current session is logged in, otherwise False.
def is_session_logged_in():
	return 'uid' in session

# Processes a login request.
# @param username	The username for the login request.
# @param password	The password for the login request.
# @return			True if the login is successful/valid, otherwise False.
def process_login_request(username, password):
	# TODO - Implement Login Here
	# For testing purposes, we will assume the username invalid is invalid and
	# all other login requests are valid.
	conn = None
	cursor = None
	try:
		conn = db_conn()
		cursor = conn.cursor()
		#cursor = conn.cursor(buffered=True)
		query = '''SELECT uid, password, password_salt FROM accounts WHERE username = (%s)''' 
		data = (username,)
		cursor.execute(query, data)
		# Username does not exist
		if cursor.rowcount <= 0:
			print('Login Error: Invalid username '+username, file=sys.stderr)
			return False
		#uid, db_passwd_hash, salt = cursor.fetchone()
		#user_passwd_hash = hashlib.sha256(password+salt)
		#print(user_passwd_hash+':'+db_passwd_hash, file=sys.stderr)
		# At this point, the login is valid
		session['uid'] = uid
		return True
	except Exception as e:
		# Some error occurred, so fail the login
		print('Login Error: exception error (user '+username+')', file=sys.stderr)
		return False
	finally:
		if conn != None:
			conn.close()
		if cursor != None:
			cursor.close()

	# Fail the login as a last resort
	print('Login Error: unknown error (user '+username+')', file=sys.stderr)
	return False

	if username == 'invalid': # TODO - Change this to check for a valid login
		# TODO - Implement invalid login handling here
		return False
	else:
		# TODO - Implement valid login handling here
		session['uid'] = 1
		return True

# Processes a logout request.
# @return			True if the logout was successful, otherwise False.
def process_logout_request():
	if not 'uid' in session:
		return False
	# TODO - Implement Logout Here
	del session['uid']
	return True



@app.route('/')
def route_index():
	if is_session_logged_in():
		return render_template('landing.html')
	else:
		return render_template('login.html')

@app.route('/login', methods=['POST'])
def route_login():
	username = request.form['username']
	password = request.form['password']
	if process_login_request(username, password) == True:
		return redirect('/')
	else:
		return redirect('/invalid_login')

@app.route('/invalid_login')
def route_invalid_login():
	if is_session_logged_in():
		redirect('/')
	else:
		return render_template('login-fail.html')

@app.route('/upload', methods=['POST'])
def route_upload():
	if is_session_logged_in():
		return render_template('upload.html')
	else:
		return render_template('login.html')
	
@app.route('/logout', methods=['POST'])
def route_logout():
	if process_logout_request() == True:
		return redirect('/')
	else:
		abort(405)

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

