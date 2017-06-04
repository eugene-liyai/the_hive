"""
    File      : manage.py
    Date      : February, 2017
    Author    : eugene liyai
    Desc      : Runs the application and initates the database
"""

# ============================================================================
# necessary imports
# ============================================================================
from flask_script import Manager

from the_hive import app
from the_hive.init_test_db import *

manager = Manager(app)

@manager.command
def initdb():

    init_bucketlist_database()


@manager.command
def populatedb():
    fill_database()
    print('Database populated')


@manager.command
def dropdb():
    drop_database_tables()
    print('Dropped the database')

if __name__ == '__main__':
    manager.run()
