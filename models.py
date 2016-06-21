from app import db
from flask_login import UserMixin
#form creation
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Required, Length, EqualTo
#hashing
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
	"""User Model"""
	__tablename__ = 'users'
	
	#used in authentication
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))
	
	#from main tutorial
	nickname = db.Column(db.String(64), index=True, unique=True)
	#email = db.Column(db.String(120), index=True, unique=True)
	#posts = db.relationship('Post', backref='author', lazy='dynamic')
	
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	
	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)
			
	def __repr__(self):
		return '<User %r>' % (self.username)
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post %r>' % (self.body)
		
class RegisterForm(Form):
	"""Registration Form"""
	username = StringField('Username', validators=[Required(),Length(1,64)])
	nickname = StringField('Username',validators=[Required(),Length(1,64)])
	password = PasswordField('Password', validators=[Required(),Length(1,64)])
	password_again = PasswordField('Password again',
		validators=[Required(), EqualTo('password')])
	submit = SubmitField('Register')
	
class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Login')
	
	#flask_login handles the remember-me quite well but no need to complicate things
	#remember_me = BooleanField('remember_me',default=False)
