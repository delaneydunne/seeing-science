from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import json
import os

'''
COMMANDS TO RUN:

>>>> export FLASK_APP=website.py
>>>> flask run
'''

'''
TODO LIST:
- LOGO
- Finish all webpages
- Make separate web pages for each level
- Properly populate content.json files
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# List all the scientific contributions
uri_list = os.listdir('static')
uri_list.remove('main.css')
uri_dict_list = [{'uri': uri} for uri in uri_list]

# Function to generate page
def make_page(uri, posts):

	@app.route('/' + uri, endpoint=uri)
	def page():
		return render_template('science.html', title=uri, posts=posts)


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', title='home')


@app.route("/levels")
def levels():
	return render_template('levels.html', title='levels')


@app.route("/quiz")
def quiz():
	return render_template('quiz.html', title='quiz')


@app.route("/menu")
def menu():
	return render_template('menu.html', title='menu', posts=uri_dict_list)
	
	
@app.route("/contribute")
def contribute():
	return render_template('contribute.html', title='contribute')


# Generate pages for each contribution
for uri in uri_list:

	filepath = 'static/' + uri + '/content.json'
	with open(filepath, 'r') as f:
		dict_list = json.load(f)
	
	make_page(uri, dict_list)


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
	app.run(debug=True)