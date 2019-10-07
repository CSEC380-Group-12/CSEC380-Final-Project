from flask import Flask, request

app = Flask(__name__)

# Session variables:
# is_logged_in		boolean: True if the session is logged in, otherwise
#					False/None
# uid				int: The UID of the user that is logged in

@app.route('/')
def route_index():
	return render_template('login.html')

@app.route('/login', method='POST')
def route_login():
	# TODO
	print("Username: "+request.form['username'])
	print("Password: "+request.form['password'])

@app.route('/logout', method='POST')
def route_logout():
	# TODO
	print(flask.session)

# vim:tabstop=4
# vim:shiftwidth=4

