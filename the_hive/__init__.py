"""
File      : the_hive.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Creates and launch the Flask application
"""

# ============================================================================
# necessary imports
# ============================================================================
import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
mail = Mail(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from the_hive.url_endpoints.url_endpoints import initialize_api_routes
initialize_api_routes(app)
