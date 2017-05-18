"""
File      : url_endpoints.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Routing url endpoints
"""
# ============================================================================
# necessary imports
# ============================================================================

from the_hive.views.view import login, add_user, index, add_job, get_user_jobs, jobs, update_users
from the_hive.views.view import page_not_found, server_error, forbiden


def initialize_api_routes(app):
    if app:
        app.add_url_rule('/', 'home', index, methods=['POST', 'GET'])
        app.add_url_rule('/login', 'login', login, methods=['POST', 'GET'])
        app.add_url_rule('/admin/add_user', 'add_user', add_user, methods=['POST', 'GET'])
        app.add_url_rule('/admin/add_job', 'add_job', add_job, methods=['POST', 'GET'])
        app.add_url_rule('/update_users/<string:user_id>', 'update_users', update_users, methods=['POST', 'GET'])
        app.add_url_rule('/admin/jobs', 'jobs', jobs, methods=['GET'])
        app.add_url_rule('/user_jobs', 'user_jobs', get_user_jobs, methods=['GET'])
        app.errorhandler(404, page_not_found)
        app.errorhandler(500, server_error)
        app.errorhandler(403, forbiden)
