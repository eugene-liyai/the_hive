"""
File      : url_endpoints.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Routing url endpoints
"""
# ============================================================================
# necessary imports
# ============================================================================
from flask import render_template

from the_hive.views.view import login, add_user, get_user_jobs, update_users, update_user_password, delete_user, users
from the_hive.views.view import update_user_access, delete_job_item, index, logout, stats, job_items, update_job_item
from the_hive.views.view import delete_job, update_job, add_job, jobs, profile, availability, add_job_item
from the_hive.views.view import rate, update_rate, help_page, update_availability, admin_reset_password


def initialize_api_routes(app):
    if app:
        app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])
        app.add_url_rule('/index', 'index', index, methods=['POST', 'GET'])
        app.add_url_rule('/login', 'login', login, methods=['POST', 'GET'])
        app.add_url_rule('/help', 'help_page', help_page, methods=['GET'])
        app.add_url_rule('/logout', 'logout', logout, methods=['GET'])
        app.add_url_rule('/admin/add_user', 'add_user', add_user, methods=['POST', 'GET'])
        app.add_url_rule('/admin/users', 'users', users, methods=['GET'])
        app.add_url_rule('/admin/add_job', 'add_job', add_job, methods=['POST', 'GET'])
        app.add_url_rule('/admin/add_job_item', 'add_job_item', add_job_item, methods=['POST', 'GET'])
        app.add_url_rule('/admin/update_job/<string:job_id>', 'update_job', update_job, methods=['POST', 'GET'])
        app.add_url_rule('/admin/update_job_item/<string:job_item_id>', 'update_job_item',
                         update_job_item, methods=['POST'])
        app.add_url_rule('/admin/delete_job/<string:job_id>', 'delete_job', delete_job, methods=['GET'])
        app.add_url_rule('/admin/delete_job_item/<string:job_item_id>',
                         'delete_job_item', delete_job_item, methods=['GET'])
        app.add_url_rule('/admin/delete_user/<string:user_id>', 'delete_user', delete_user, methods=['GET'])
        app.add_url_rule('/admin/rates', 'rate', rate, methods=['GET'])
        app.add_url_rule('/admin/reset_password/<string:user_id>', 'admin_reset_password',
                         admin_reset_password, methods=['GET'])
        app.add_url_rule('/profile', 'profile', profile, methods=['GET'])
        app.add_url_rule('/stats', 'stats', stats, methods=['GET', 'POST'])
        app.add_url_rule('/availability', 'availability', availability, methods=['GET', 'POST'])
        app.add_url_rule('/update_availability/<string:user_id>', 'update_availability',
                         update_availability, methods=['GET'])
        app.add_url_rule('/update_user_access/<string:user_id>', 'update_user_access',
                         update_user_access, methods=['GET'])
        app.add_url_rule('/admin/update_rate/<string:rate_id>', 'update_rate', update_rate, methods=['GET', 'POST'])
        app.add_url_rule('/admin/update_users/<string:user_id>', 'update_users', update_users, methods=['POST', 'GET'])
        app.add_url_rule('/update_user/<string:user_id>', 'update_users', update_users, methods=['POST', 'GET'])
        app.add_url_rule('/update_password/<string:user_id>', 'update_user_password', update_user_password,
                         methods=['POST', 'GET'])
        app.add_url_rule('/admin/jobs', 'jobs', jobs, methods=['GET'])
        app.add_url_rule('/admin/job_items', 'job_items', job_items, methods=['GET', 'POST'])
        app.add_url_rule('/user_jobs', 'user_jobs', get_user_jobs, methods=['GET'])

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def server_error(e):
            return render_template('500.html'), 500

        @app.errorhandler(403)
        def server_error(e):
            return render_template('403.html'), 403
