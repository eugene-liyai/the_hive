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

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
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
def load_user(userid):
    return Users.query.get(int(userid))


def index():
    if current_user:
        return render_template('dashboard.html', user=current_user)
    else:
        return render_template('index.html')


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
                flash("Logged in successfully as {}".format(user.username))
                return redirect(request.args.get('next') or url_for('user', username=user.username))
            flash('Incorrect username or password')
        return render_template("login.html")
    except:
        flash('Error communicating with the server')
        return render_template("login.html")


@login_required
def add_user():
    """
    
    The method adds a new user to the application.

    :return: returns success message if method executes successfully
    """
    if request.method == 'POST':
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
def add_job():
    """

    The method adds new job to the application.

    :return: returns success message if methodexecutes successfuly
    """
    if request.method == 'POST':
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


