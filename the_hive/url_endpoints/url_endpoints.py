"""
File      : url_endpoints.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Routing url endpoints
"""
# ============================================================================
# necessary imports
# ============================================================================

from the_hive.views.view import login, add_user, get_user_jobs, update_users, update_user_password, delete_user, users
from the_hive.views.view import page_not_found, server_error, forbiden, index, logout
from the_hive.views.view import delete_job, update_job, add_job, jobs
from the_hive.views.view import rate, update_rate


def initialize_api_routes(app):
    if app:
        app.add_url_rule('/', 'home', index, methods=['POST', 'GET'])
        app.add_url_rule('/index', 'home', index, methods=['POST', 'GET'])
        app.add_url_rule('/login', 'login', login, methods=['POST', 'GET'])
        app.add_url_rule('/logout', 'logout', logout, methods=['GET'])
        app.add_url_rule('/admin/add_user', 'add_user', add_user, methods=['POST', 'GET'])
        app.add_url_rule('/admin/users', 'users', users, methods=['GET'])
        app.add_url_rule('/admin/add_job', 'add_job', add_job, methods=['POST', 'GET'])
        app.add_url_rule('/admin/update_job/<string:job_id>', 'update_job', update_job, methods=['POST', 'GET'])
        app.add_url_rule('/admin/delete_job/<string:job_id>', 'delete_job', delete_job, methods=['GET'])
        app.add_url_rule('/admin/delete_user/<string:user_id>', 'delete_user', delete_user, methods=['GET'])
        app.add_url_rule('/admin/rates', 'rate', rate, methods=['GET'])
        app.add_url_rule('/admin/update_rate', 'update_rate', update_rate, methods=['GET', 'POST'])
        app.add_url_rule('/update_users/<string:user_id>', 'update_users', update_users, methods=['POST', 'GET'])
        app.add_url_rule('/update_password/<string:user_id>', 'update_user_password', update_user_password,
                         methods=['POST', 'GET'])
        app.add_url_rule('/admin/jobs', 'jobs', jobs, methods=['GET'])
        app.add_url_rule('/user_jobs', 'user_jobs', get_user_jobs, methods=['GET'])
        # app.error_handler_spec[None][404] = page_not_found
        # app.error_handler_spec[None][500] = server_error
        # app.error_handler_spec[None][403] = forbiden
