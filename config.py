import os
from utils import format_datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy_utils import database_exists, create_database


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'postgres://postgres:postgres@localhost:5432/fyyur'

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

app.jinja_env.auto_reload = True
app.jinja_env.filters['datetime'] = format_datetime

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)

if not database_exists(DATABASE_URI):
    create_database(DATABASE_URI)
