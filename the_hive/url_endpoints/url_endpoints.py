"""
File      : url_endpoints.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Routing url endpoints
"""
# ============================================================================
# necessary imports
# ============================================================================

from the_hive.views.view import login, add_user, index, add_job


def initialize_api_routes(app):
    if app:
        app.add_url_rule('/', 'home', index, methods=['POST', 'GET'])
        app.add_url_rule('/login', 'login', login, methods=['POST', 'GET'])
        app.add_url_rule('/add_user', 'add_user', add_user, methods=['POST', 'GET'])
        app.add_url_rule('/add_job', 'add_job', add_job, methods=['POST', 'GET'])