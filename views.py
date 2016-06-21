from flask import render_template, flash, redirect, url_for, g
from app import app
from .models import LoginForm, RegisterForm, User
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
#make db accessible
from app import db, lm

#any function decorated with before_request will run before the view function each time 
#a request is received.
@app.before_request
def before_request():
	g.user = current_user


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		
		#confirm password matches
		if user is None or not user.verify_password(form.password.data):
			flash('invalid username or password')
			return redirect(url_for('login'))
		#log user in
		login_user(user)
		flash('you are logged in!')
		
		#flash('username="%s", password=%s' % 
			#(user.username.data , user.password.data))
		return redirect('/index') 
	
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	"""User logout route."""
	logout_user()
	return redirect(url_for('index'))
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	"""The way a user registers"""
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		
		if user is not None:
			flash('username already exists.')
			return redirect(url_for('register'))
		#add new user to database
		user = User(username=form.username.data, password=form.password.data, 
			nickname=form.nickname.data)
		db.session.add(user)
		db.session.commit()
		#return redirect(url_for('index'))
	return render_template('register.html',form=form)

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User %s not found.' % nickname)
		#return redirect(url_for('index', nickname=nickname))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)

#user loader
@lm.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))	
