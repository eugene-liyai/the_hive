"""
File      : controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Controller file processes request from the url endpoints
"""

# ============================================================================
# necessary imports
# ============================================================================
import os
from math import ceil

from datetime import datetime, timedelta, date
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, logout_user, current_user

from the_hive import login_manager
from the_hive.controllers.database_controller import DatabaseController
from the_hive.models.users import Users

#
# Database engine
# Postgres connection postgresql+psycopg2://user:password@host/database
#
db_engine = os.environ['THE_HIVE_SQLALCHEMY_DATABASE_URI']

PAGE_SIZE = 10

DATA_CONTROLLER = DatabaseController(db_engine)


def initialize_database():
    """

    The method initializes tables and relations in the database.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.initialize_database()


def populate_database():
    """

    The method populates database tables with valid data.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.populate_database()


def drop_tables():
    """

    The method drops tables and relations in the database.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.drop_tables()


@login_manager.user_loader
def load_user(user_id):
    return DATA_CONTROLLER.get_user_by_id(user_id)[0]


def login():
    """

    The method validates user credentials and gives user access.

    :param email: user email
    :param password: user password
    :return: Json format or plain text depending in the serialize parameter
    """

    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            validation_return = DATA_CONTROLLER.user_login_authentication(email=email, password=password)
            if validation_return['status']:
                user = validation_return['User']
                login_user(user, True)
                flash("Logged in successfully as {}".format(user.email))
                return redirect(request.args.get('next') or url_for('index'))
            flash('Incorrect email or password')
        return render_template("index.html")
    except Exception as e:
        print(e)
        flash('Error communicating with the server')
        return render_template("index.html")


@login_required
def index():
    if current_user.role == 'ROLE_ADMIN':
        agents = DATA_CONTROLLER.get_user_by_id()
        return render_template('adminUserJobs.html', user=current_user, users=agents)
    elif current_user.role == 'ROLE_AGENT':
        return render_template('userJobs.html', user=current_user)
    return render_template('index.html')


@login_required
def logout():
    """

    The method logs out user currently in session.

    :return: redirects to login page
    """
    logout_user()
    return redirect(url_for('index'))


@login_required
def add_user():
    """
    
    The method adds a new user to the application.

    :return: returns success message if method executes successfully
    """
    if current_user.role != 'ROLE_ADMIN':
        return abort(403)
    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        add_user_response = DATA_CONTROLLER.create_user(first_name, last_name, email, password, role)
        if add_user_response:
            flash("successfully added user {} {}".format(first_name, last_name))
    return render_template("add_user.html")


@login_required
def delete_user(user_id):
    """

    The method deletes user with the provided id.

    :param user_id: id of the user to be deleted
    :return: http response
    """
    if current_user.role != 'ROLE_ADMIN':
        return abort(403)
    try:
        if DATA_CONTROLLER.delete_user(user_id):
            flash("deleted job '{}'".format(user_id))
            return redirect(url_for('users'))
        else:
            flash("failed to delete job '{}'".format(user_id))
            return redirect(url_for('users'))
    except ValueError as err:
        print(err)
        flash("Error communicating with the server")
        return redirect(url_for('users'))


@login_required
def users(user_id=None):
    """

    The method returns user(s).

    :param user_id: user id intended to be searched
    :return: list of user(s) in the database
    """

    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    users = DATA_CONTROLLER.get_user_by_id(user_id=user_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(users)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return abort(404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        users = users[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    return render_template('users.html', user=current_user, pages=pages, users=users)


@login_required
def profile():
    """
    
    The method returns the logged in user credentials
    
    :return: returns user information
    """

    if current_user.user_id:
        user = DATA_CONTROLLER.get_user_by_id(user_id=current_user.user_id, serialize=True)

        if len(user):
            return render_template('profile.html', user=user[0])
        else:
            return abort(500)


@login_required
def stats():
    """
    
    The method returns user's job stats.
    
    :return: 
    """
    if current_user.user_id:
        job_rate = DATA_CONTROLLER.get_rate_by_id()[0].rate
        total_jobs = 0
        total_revenue = 0
        total_paid = 0
        job_within_a_month = 0
        past_30_days = date.today() + timedelta(-30)

        for job in current_user.user_detail:
            total_jobs += 1
            total_revenue = total_revenue + (job.duration * job_rate)
            if job.paid:
                total_paid = total_paid + (job.duration * job_rate)

            if job.date_completed and job.date_completed > past_30_days:
                datetime.combine(job.date_completed, datetime.min.time())
                job_within_a_month += 1

        return render_template('stats.html', user=current_user,
                               total_jobs=total_jobs,
                               total_revenue=total_revenue,
                               total_paid=total_paid,
                               job_within_a_month=job_within_a_month)


@login_required
def update_users(user_id):
    """

    The method updates existing user to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST':

        new_user = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "role": request.form["role"],
            "date_modified": datetime.utcnow()
        }

        try:
            if user_id == current_user.user_id or current_user.role == 'ROLE_ADMIN':
                DATA_CONTROLLER.update_user(user_id, new_user)
                flash("updated user {} {}".format(request.form["first_name"], request.form["last_name"]))
                return render_template('update_user.html')
            else:
                return render_template('403.html'), 403
        except Exception as ex:
            print(ex)
            flash("Error updating user {} {}".format(request.form["first_name"], request.form["last_name"]))
            return render_template('update_user.html')

    else:
        user = DATA_CONTROLLER.get_user_by_id(user_id)
        return render_template('update_user.html', user=user)


@login_required
def update_user_password(user_id):
    """

    The method updates existing user to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST':
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            flash("password provided does not match")
            return render_template('update_user.html')

        new_user = {
            "password": password
        }

        try:
            if user_id == current_user.user_id or current_user.role == 'ROLE_ADMIN':
                DATA_CONTROLLER.update_password(user_id, new_user)
                flash("updated password")
                return render_template('update_user.html')
            else:
                return render_template('403.html'), 403
        except Exception as ex:
            print(ex)
            flash("Error updating user {} {}".format(request.form["first_name"], request.form["last_name"]))
            return render_template('update_user.html')

    else:
        user = DATA_CONTROLLER.get_user_by_id(user_id)
        return render_template('update_user.html', user=user)


@login_required
def add_job():
    """

    The method adds new job to the application.

    :return: returns success message if method executes successfully
    """
    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':
        job_name = request.form['job_name']
        job_id = request.form['job_id']
        verbatim = request.form['verbatim']
        timestamp = request.form['timestamp']
        duration = request.form['duration']
        description = request.form['description']
        user = request.form['user']
        try:
            job_id_response = DATA_CONTROLLER.create_job(job_id,
                                               job_name,
                                               verbatim,
                                               timestamp,
                                               duration,
                                               description,
                                               user)
            flash("Added job '{}'".format(job_id_response))
            return render_template('add_job.html')
        except Exception as ex:
            print(ex)
            flash("Error adding job '{}'".format(job_id))
            return render_template('add_job.html')
    return render_template('add_job.html')


@login_required
def update_job(job_id):
    """

    The method updates existing job to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':

        date_completed = None
        if request.form["competed"] is True:
            date_completed = datetime.now()

        new_job = {
            "job_name": request.form["job_name"],
            "date_completed": date_completed,
            "competed": request.form["competed"],
            "verbatim": request.form["verbatim"],
            "timestamp": request.form["timestamp"],
            "duration": request.form["duration"],
            "description": request.form["description"],
            "user": request.form["user"]
        }

        try:
            DATA_CONTROLLER.update_job(job_id, new_job)
            flash("updated job '{}'".format(job_id))
            return redirect(url_for('jobs'))
        except Exception as ex:
            print(ex)
            flash("Error updating job '{}'".format(job_id))
            return redirect(url_for('jobs'))


@login_required
def help_page():
    """

    The method returns help messages.

    :return: job rate(s)
    """

    return render_template('help.html', user=current_user)

@login_required
def jobs(job_id=None):
    """

    The method returns job(s).

    :param serialize: Serialize helps indicate the format of the response
    :param job_id: job id intended to be searched
    :return: Json format or plain text depending in the serialize parameter
    """

    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    jobs = DATA_CONTROLLER.get_job_by_id(job_id=job_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(jobs)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return abort(404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        jobs = jobs[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    return render_template('jobs.html',
                           user=current_user,
                           pages=pages,
                           jobs=jobs)


@login_required
def job_items(item_id=None):
    """

    The method returns job(s).

    :param serialize: Serialize helps indicate the format of the response
    :param item_id: item id intended to be searched
    :return: Json format or plain text depending in the serialize parameter
    """

    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    jobs = DATA_CONTROLLER.get_item_by_id(item_id=item_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(jobs)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return abort(404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        jobs = jobs[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    return render_template('jobsItems.html',
                           user=current_user,
                           pages=pages,
                           job_items=jobs)


@login_required
def get_user_jobs(job_id=None):
    """

    The method returns job(s).

    :param serialize: Serialize helps indicate the format of the response
    :param job_id: job id intended to be searched
    :return: Json format or plain text depending in the serialize parameter
    """
    jobs = DATA_CONTROLLER.get_user_job_by_id(job_id=job_id, user=current_user.user_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(jobs)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return abort(404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        jobs = jobs[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

        return render_template('jobs.html', pages=pages, jobs=jobs)


@login_required
def delete_job(job_id):
    """

    The method deletes job with the provided id.

    :param job_id: id of the job to be deleted
    :return: http response
    """
    if current_user.role == 'ROLE_ADMIN':
        try:
            if DATA_CONTROLLER.delete_job(job_id):
                flash("deleted job '{}'".format(job_id))
                return redirect(url_for('jobs'))
            else:
                flash("failed to delete job '{}'".format(job_id))
                return redirect(url_for('jobs'))
        except ValueError as err:
            print(err)
            flash("Error communicating with the server")
            return redirect(url_for('jobs'))
    else:
        return render_template('403.html'), 403


@login_required
def user_profile(user_id):
    if current_user.user_id == user_id or current_user.role == 'ROLE_ADMIN':
        return render_template('user.html', user=current_user)
    else:
        return render_template('403.html'), 403


@login_required
def update_rate(rate_id):
    """

    The method updates existing rate to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':

        new_rate = {
            "rate": request.form["rate"],
            "description": request.form["description"]
        }

        try:
            DATA_CONTROLLER.update_rate(rate_id, new_rate)
            flash("updated rate '{}'".format(rate_id))
            return redirect(url_for('rate'))
        except Exception as ex:
            print(ex)
            flash("Error updating rate '{}'".format(rate_id))
            return redirect(url_for('rate'))


@login_required
def rate(rate_id=None):
    """

    The method returns job rate(s).

    :param rate_id: rate id intended to be searched
    :return: job rate(s)
    """

    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    rates = DATA_CONTROLLER.get_rate_by_id(rate_id=rate_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []

    if page:
        number_of_pages = int(ceil(float(len(rates)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return abort(404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        rates = rates[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    return render_template('rates.html', user=current_user, pages=pages, rates=rates)


@login_required
def availability():
    return render_template('availability.html', user=current_user)


def page_not_found(e):
    return render_template('404.html'), 404


def server_error(e):
    return render_template('500.html'), 500


def forbiden(e):
    return render_template('403.html'), 403
