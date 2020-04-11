# This page initialize everything
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create/initialization of the application
app = Flask(__name__)
# upload the configuration values from file config.py
app.config.from_pyfile('config.py')
# create database
db = SQLAlchemy(app)


from application_files import views
