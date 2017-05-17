import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from the_hive.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from the_hive.url_endpoints import url_endpoints

