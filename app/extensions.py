# Flask-SQLAlchemy extension instance
from flask_sqlalchemy import SQLAlchemy
# Flask-Login
from flask_login import LoginManager
# Flask-WTF csrf protection
from flask_wtf.csrf import CsrfProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CsrfProtect()