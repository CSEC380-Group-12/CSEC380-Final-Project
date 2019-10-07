from flask import *

app = Flask(__name__)

# Session variables:
# uid				int: The UID of the user that is logged in

# Checks if the current session is logged in.
# @return			True if the current session is logged in, otherwise False.
def is_session_logged_in():
	# TODO - Make this actually check if the session is logged in
	return True

# Processes a login request.
# @param username	The username for the login request.
# @param password	The password for the login request.
# @return			True if the login is successful/valid, otherwise False.
def process_login_request(username, password):
	# TODO - Implement Login Here
	# For testing purposes, we will assume the username invalid is invalid and
	# all other login requests are valid.
	if username == 'invalid': # TODO - Change this to check for a valid login
		# TODO - Implement invalid login handling here
		return False
	else:
		# TODO - Implement valid login handling here
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
		return redirect('/invalid_login')
	else:
		return redirect('/')

@app.route('/invalid_login')
def route_invalid_login():
	return render_template('login-fail.html')

@app.route('/logout', methods=['POST'])
def route_logout():
	# TODO - Implement Logout Here
	print(session)
	return "<h1>Logout has not been implemented yet</h1>"

@app.route('/LoginCSS.css')
def route_LoginCSS():
	return app.send_static_file('LoginCSS.css')

@app.route('/LandingCSS.css')
def route_LandingCSS():
	return app.send_static_file('LandingCSS.css')

# vim:tabstop=4
# vim:shiftwidth=4

