from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user

#bootstrap


app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

# create database tables if they don't exist yet
db.create_all()

from app import views, models






