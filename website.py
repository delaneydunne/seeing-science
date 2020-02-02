from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import json

'''
COMMANDS TO RUN:

>>>> export FLASK_APP=website.py
>>>> flask run
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# List all the scientific contributions
uri_list = ['ligo']
#uri_list = ['ligo', 'bean']
#https://stackoverflow.com/questions/33372054/get-folder-name-of-the-file-in-python

# Function to generate page
def make_page(uri, posts):

	@app.route('/' + uri)
	def page():
		return render_template('science.html', title=uri, posts=posts)


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', title='Home')


@app.route("/levels")
def levels():
	return render_template('levels.html', title='Levels')


@app.route("/menu")
def menu():
	return render_template('menu.html', title='Menu')


# Generate pages for each contribution
for uri in uri_list:

	filepath = 'seeing_science/papers/' + uri + '/content.json'
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