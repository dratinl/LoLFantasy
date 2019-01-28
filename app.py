from flask import Flask 
from flask import render_template
from flask import request
import json

app = Flask(__name__)
@app.route('/')
def hello():
	return render_template('signin.html')

@app.route('/draft')
def drafty():
	return render_template('draft.html')

@app.route('/drafttool', methods=['POST'])
def signupDrafter():
	user_name = request.form['username']
	#team_name = request.form['teamname']
	response = json.dumps({'status':'OK', 'username':user_name,}) #'teamname': team_name})
	return response

if __name__== "__main__":
	app.run()