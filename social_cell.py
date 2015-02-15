from flask import  redirect, Flask, render_template, url_for, request
from flask_oauth import OAuth
from string import Template
import json
from flask import session
from rauth.service import OAuth2Service
from flask_sqlalchemy import SQLAlchemy
import database
oauth = OAuth()
app = Flask(__name__)

database_args = {'host':'localhost', 'user': 'social_cell', 'password':'social_cell', 'database':'social_cell'}
db = database.Database(database_args)

try:
	if db:
		client_id = db.sql(""" select defvalue from `tabConfiguration Details` where 
			defattr ='fb_client_id'""")
		if client_id:
			FB_CLIENT_ID =  client_id[0][0]

		client_secret = db.sql(""" select defvalue from `tabConfiguration Details` where 
			defattr ='fb_client_secret'""")
		if client_secret:
			FB_CLIENT_SECRET =  client_secret[0][0]

	if FB_CLIENT_SECRET and FB_CLIENT_ID:
		graph_url = 'https://graph.facebook.com/'
		facebook = OAuth2Service(name='facebook',
		                         authorize_url='https://www.facebook.com/dialog/oauth',
		                         access_token_url=graph_url + 'oauth/access_token',
		                         client_id=FB_CLIENT_ID,
		                         client_secret=FB_CLIENT_SECRET,
		                         base_url=graph_url)
except Exception, e:
	print e

@app.route('/')
def webprint():
	app.secret_key = 'why would I tell you my secret key?'
	if FB_CLIENT_ID and FB_CLIENT_SECRET:
		return render_template('login.html')
	else:
		return render_template('credential.html')

@app.route('/oauth_credentials', methods=['GET', 'POST'])
def oauth_credentials():
	try:
		args = {'fb_client_id': request.form['client_id'], 'fb_client_secret': request.form['client_secret']}
		if db:
			for details in args:
				db.sql(""" insert into `tabConfiguration Details` values('%s', '%s')"""%(details, args[details]), auto_commit=1)
			return render_template('login.html')
	except Exception, e:
		return e

@app.route('/login', methods=['GET', 'POST'])
def login():
	try:
		redirect_uri = url_for('authorized', _external=True)
		params = {'redirect_uri': redirect_uri}
		return redirect(facebook.get_authorize_url(**params))
	except Exception, e:
		print e

@app.route('/authorized')
def authorized():
	try:
		redirect_uri = url_for('authorized', _external=True)
		data = dict(code=request.args['code'], redirect_uri=redirect_uri)
		session = facebook.get_auth_session(data=data)
		me = session.get('me').json()
		return "Logged in as %s"%(me.get('name'))
	except Exception, e:
		print e
	

if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = 8080)
