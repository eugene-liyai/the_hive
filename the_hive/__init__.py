"""
File      : the_hive.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Creates and launch the Flask application
"""

# ============================================================================
# necessary imports
# ============================================================================
from flask import Flask
from flask_login import LoginManager

from the_hive.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from the_hive.url_endpoints.url_endpoints import initialize_api_routes
initialize_api_routes(app)
