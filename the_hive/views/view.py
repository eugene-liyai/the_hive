# -*- coding:utf-8 -*-
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
from the_hive.util import *
from the_hive.controllers.email_controller import send_email

#
# Database engine
# Postgres connection postgresql+psycopg2://user:password@host/database
#
db_engine = os.environ['THE_HIVE_SQLALCHEMY_DATABASE_URI']

PAGE_SIZE = 10

DATA_CONTROLLER = DatabaseController(db_engine)

# administrator list
ADMINS = ['info@bhiveweb.com']


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
        jobs = DATA_CONTROLLER.get_job_by_id(job_id=None, serialize=True)
        return render_template('userJobs.html', user=current_user, jobs=jobs)
    return render_template('index.html')


@login_required
def logout():
    """

    The method logs out user currently in session.

    :return: redirects to login page
    """
    flash('Logout successful')
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

        if is_email_valid(email) is False:
            flash("Email provided is not valid")
            return redirect(url_for('users'))

        if has_white_space(first_name) or has_white_space(last_name):
            flash("Names cannot have white space")
            return redirect(url_for('users'))

        password = generate_random_password_string()
        add_user_response = DATA_CONTROLLER.create_user(first_name, last_name, email, password, role)
        if add_user_response:
            flash("successfully added user {} {}".format(first_name, last_name))
        else:
            flash("unable to add user {} {}".format(first_name, last_name))
    return redirect(url_for('users'))


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
            flash("deleted user '{}'".format(user_id))
            return redirect(url_for('users'))
        else:
            flash("failed to delete user '{}'".format(user_id))
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

        new_user = {}

        # Admin update directive
        if current_user.role == "ROLE_ADMIN":

            if is_email_valid(request.form["edit_email"]) is False:
                flash("Email provided is not valid")
                return redirect(url_for('users'))

            if has_white_space(request.form["edit_first_name"]) or has_white_space(request.form["edit_last_name"]):
                flash("Names cannot have white space")
                return redirect(url_for('users'))

            role = 'ROLE_AGENT'
            if request.form["edit_role"] == 'admin':
                role = 'ROLE_ADMIN'

            new_user = {
                "first_name": request.form["edit_first_name"],
                "last_name": request.form["edit_last_name"],
                "email": request.form["edit_email"],
                "role": role,
                "date_modified": datetime.utcnow()
            }
        # User update directive
        else:
            if is_email_valid(request.form["edit_email"]) is False:
                flash("Email provided is not valid")
                return redirect(url_for('profile'))

            if has_white_space(request.form["edit_first_name"]) or has_white_space(request.form["edit_last_name"]):
                flash("Names cannot have white space")
                return redirect(url_for('profile'))

            new_user = {
                "first_name": request.form["edit_first_name"],
                "last_name": request.form["edit_last_name"],
                "email": request.form["edit_email"],
                "date_modified": datetime.utcnow()
            }

        try:
            if current_user.user_id == int(user_id) or current_user.role == 'ROLE_ADMIN':
                DATA_CONTROLLER.update_user(user_id, new_user)
                flash("updated user {} {}".format(request.form["edit_first_name"], request.form["edit_last_name"]))
                if current_user.role == 'ROLE_ADMIN':
                    return redirect(url_for('users'))
                return redirect(url_for('profile'))
            else:
                return render_template('403.html'), 403
        except Exception as ex:
            print(ex)
            flash("Error updating user {} {}".format(request.form["edit_first_name"], request.form["edit_last_name"]))
            return redirect(url_for('users'))

    return redirect(url_for('users'))


@login_required
def update_user_password(user_id):
    """

    The method updates existing user to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST':
        current_password = request.form["current_password"]
        password = request.form["new_password"]
        confirm_password = request.form["confirm_new_password"]

        if current_password == '' \
                or current_password is None \
                or password == ''\
                or password is None \
                or confirm_password == '' \
                or confirm_password is None:
            flash("Fields cannot be blank")
            return redirect(url_for('profile'))

        if current_user.check_user_password(current_password) is False:
            flash("Current password does not match this account's password")
            return redirect(url_for('profile'))

        if len(password) <= 6:
            flash("Password must be at least 7 characters long")
            return redirect(url_for('profile'))

        if password != confirm_password:
            flash("password provided does not match")
            return redirect(url_for('profile'))

        if password == current_password:
            flash("new password cannot be same as current password")
            return redirect(url_for('profile'))

        new_user = {
            "password": password
        }

        try:
            if int(user_id) == current_user.user_id or current_user.role == 'ROLE_ADMIN':
                DATA_CONTROLLER.update_password(user_id, new_user)
                flash("updated password")
                return redirect(url_for('profile'))
            else:
                return render_template('403.html'), 403
        except Exception as ex:
            print(ex)
            flash("Error updating password for {} {}".format(current_user.first_name, current_user.last_name))
            return redirect(url_for('profile'))

    else:
        return redirect(url_for('profile'))


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
        verbatim = request.form.get('verbatim')
        timestamp = request.form.get('timestamp')
        duration = request.form['duration']
        link = request.form['link']
        description = request.form['description']

        if is_numbers_only(duration) is False:
            flash("Duration can only be an integer")
            return redirect(url_for('jobs'))
        elif has_white_space(job_id):
            flash("Job ID cannot contain white space")
            return redirect(url_for('jobs'))

        try:
            job_id_response = DATA_CONTROLLER.create_job(job_id,
                                                         job_name,
                                                         verbatim,
                                                         timestamp,
                                                         duration,
                                                         link,
                                                         description)
            flash("Added job '{}'".format(job_id_response))
            return redirect(url_for('jobs'))
        except Exception as ex:
            print(ex)
            flash("Error adding job '{}'".format(job_id))
            return redirect(url_for('jobs'))
    return redirect(url_for('jobs'))


@login_required
def add_job_item():
    """

    The method adds new job to the application.

    :return: returns success message if method executes successfully
    """
    if current_user.role != 'ROLE_ADMIN':
        return abort(403)

    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':

        job_name = request.form['job_item_name']
        user_assign = request.form['user_assign']
        duration = request.form.get('item_duration')
        description = request.form.get('item_description')
        user_assign_email = DATA_CONTROLLER.get_user_by_id(int(user_assign))

        if is_numbers_only(duration) is False:
            flash("Duration can only be an integer")
            return redirect(url_for('job_items'))

        parent_job_detail = DATA_CONTROLLER.get_job_by_id(job_id=job_name)
        link = parent_job_detail[0].download_link
        if is_job_duration_item_invalid(parent_job_detail[0], int(duration)):
            flash("The job duration is invalid, does not match parent")
            return redirect(url_for('job_items'))

        try:
            user_job_notification(current_user,
                                  user_assign_email[0],
                                  link)
            job_id_response = DATA_CONTROLLER.create_job_item(job_name,
                                                              user_assign,
                                                              duration,
                                                              link,
                                                              description)
            flash("Added job item '{}'".format(job_id_response))
            return redirect(url_for('job_items'))
        except Exception as ex:
            print(ex)
            flash("Error adding job item under '{}'".format(job_name))
            return redirect(url_for('job_items'))
    return redirect(url_for('job_items'))


@login_required
def update_job(job_id):
    """

    The method updates existing job to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':

        if is_numbers_only(request.form["edit_duration"]) is False:
            flash("Duration can only be an integer")
            return redirect(url_for('jobs'))
        elif has_white_space(request.form["edit_job_id"]):
            flash("Job ID cannot contain white space")
            return redirect(url_for('jobs'))

        timestamp = False
        verbatim = False
        if request.form.get("edit_timestamp"):
            timestamp = True
        if request.form.get("edit_verbatim"):
            verbatim = True

        new_job = {
            "job_id": request.form["edit_job_id"],
            "verbatim": verbatim,
            "timestamp": timestamp,
            "duration": request.form["edit_duration"],
            "description": request.form["edit_description"],
            "link": request.form["edit_link"]
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
def update_job_item(job_item_id):
    """

    The method updates existing job item to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST' and current_user.role == 'ROLE_ADMIN':

        date_completed = None
        complete = False
        paid = False
        if request.form["progress"] == 'complete':
            date_completed = datetime.now()
            complete = True

        if request.form["pay-status"] == 'paid':
            paid = True

        if is_numbers_only(request.form["edit_item_duration"]) is False:
            flash("Duration can only be an integer")
            return redirect(url_for('job_items'))

        parent_job_detail = DATA_CONTROLLER.get_job_by_id(job_id=request.form["job_name"])
        user_assign_email = DATA_CONTROLLER.get_user_by_id(int(request.form["user"]))
        if is_job_duration_invalid(parent_job_detail[0],
                                   int(request.form["edit_item_duration"]),
                                   int(request.form["job_item_id"])):
            flash("The job duration is invalid, does not match parent")
            return redirect(url_for('job_items'))

        if paid and complete is False:
            flash("Cannot mark job as paid while job still in progress")
            return redirect(url_for('job_items'))

        new_job = {
            "date_completed": date_completed,
            "competed": complete,
            "duration": request.form["edit_item_duration"],
            "description": request.form["edit_item_description"],
            "user": request.form["user"],
            "paid": paid
        }
        try:
            user_job_notification(current_user,
                                  user_assign_email[0],
                                  parent_job_detail[0].download_link)
            DATA_CONTROLLER.update_job_item(job_item_id, new_job)
            if paid and check_if_job_should_be_marked_as_paid(parent_job_detail[0], job_item_id):
                DATA_CONTROLLER.update_paid_job(parent_job_detail[0].job_id)
            flash("updated job item '{}'".format(job_item_id))
            return redirect(url_for('job_items'))
        except Exception as ex:
            print(ex)
            flash("Error updating job item '{}'".format(job_item_id))
            return redirect(url_for('job_items'))


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

    jobs = DATA_CONTROLLER.get_item_by_id(item_id=item_id, serialize=False)
    users = DATA_CONTROLLER.get_user_by_id(serialize=True)
    rates = DATA_CONTROLLER.get_rate_by_id(serialize=True)[0]
    all_inprogress_jobs = DATA_CONTROLLER.get_job_not_completed(serialize=True)
    agents = DATA_CONTROLLER.get_available_users(serialize=True)
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
                           job_items=jobs,
                           users=users,
                           rates=rates,
                           inprogress=all_inprogress_jobs,
                           agents=agents)


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
            delete_response = DATA_CONTROLLER.delete_job(job_id)
            if delete_response:
                flash("deleted job '{}'".format(job_id))
                return redirect(url_for('jobs'))
            else:
                flash("Error deleting job '{}'".format(job_id))
                return redirect(url_for('jobs'))
        except ValueError as err:
            print(err)
            flash("Error communicating with the server")
            return redirect(url_for('jobs'))
    else:
        return render_template('403.html'), 403


@login_required
def delete_job_item(job_item_id):
    """

    The method deletes job with the provided id.

    :param job_item_id: id of the job item to be deleted
    :return: http response
    """
    if current_user.role == 'ROLE_ADMIN':
        try:
            delete_response = DATA_CONTROLLER.delete_job_item(job_item_id)
            if delete_response:
                flash("deleted job item '{}'".format(job_item_id))
                return redirect(url_for('job_items'))
            else:
                flash("Error deleting item '{}'".format(job_item_id))
                return redirect(url_for('job_items'))
        except ValueError as err:
            print(err)
            flash("Error communicating with the server")
            return redirect(url_for('job_items'))
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

        if has_white_space(request.form["edit_rate"]):
            flash("Fields cannot have white space")
            return redirect(url_for('rate'))

        if is_numbers_only(request.form["edit_rate"]) is False:
            flash("Rate must be an integer")
            return redirect(url_for('rate'))

        new_rate = {
            "rate": request.form["edit_rate"],
            "description": request.form["edit_description"]
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


@login_required
def update_availability(user_id):
    """

    The method updates user availability.

    :param user_id: user id intended to be updated
    :return: update status
    """

    if current_user.user_id == int(user_id):
        try:
            if DATA_CONTROLLER.update_availability(user_id):
                flash("Updated user availability")
                return redirect(url_for('availability'))
            flash("Unable to update user availability")
            return redirect(url_for('availability'))
        except:
            flash("Error updating availability")
            return redirect(url_for('availability'))
    else:
        return abort(401)


@login_required
def update_user_access(user_id):
    """

    The method updates user availability.

    :param user_id: user id intended to be updated
    :return: update status
    """

    if current_user.role == 'ROLE_ADMIN':
        try:
            if DATA_CONTROLLER.update_user_access(user_id):
                flash("Updated user access to platform")
                return redirect(url_for('users'))
            flash("Unable to update user access")
            return redirect(url_for('users'))
        except:
            flash("Error updating user access")
            return redirect(url_for('users'))
    else:
        return abort(401)


def user_job_notification(sender, recipient, file):
    send_email("the-hive Email Alert",
               ADMINS[0],
               [recipient.email, sender.email],
               render_template("notificationTemplate.html", recipient=recipient, file=file))


def page_not_found(e):
    return render_template('404.html'), 404


def server_error(e):
    return render_template('500.html'), 500


def forbiden(e):
    return render_template('403.html'), 403
