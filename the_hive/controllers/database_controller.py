"""
File      : database_controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Acts as a service file for database population and db engine to be used
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from the_hive.models.users import Users
from the_hive.models.jobs import Jobs
from the_hive.models.rate import Rate
from the_hive.models.job_details import JobsDetails
from the_hive.models.initialize_db import init_bucketlist_database, drop_bucketlist_database


class DatabaseController:

    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of Database Controller class
        :type engine: string
        """
        if not engine:
            raise ValueError('The parameters specified in engine string are not supported by SQLAlchemy')
        self.engine = engine
        db_engine = create_engine(engine)
        self.db_engine = db_engine
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()

    def initialize_database(self):
        """
        Initializes the database tables and relationships
        :return: String
        """
        init_bucketlist_database(self.engine)
        return 'Database Initialized'

    def drop_tables(self):
        """
        drops the database tables and relationships
        :return: String
        """
        drop_bucketlist_database(self.db_engine)
        return 'Database Dropped'

    def create_user(self, first_name, last_name, email, password, role):
        """

        The method creates and saves a new user to the database.

        :param first_name: First Name of the new user
        :param last_name: Last Name of the new user
        :param email: Email address of the new user
        :param role: role selected by the new user
        :param password: Password for the new user
        :return: True if user was created and false
        """
        try:
            new_user = Users(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
            self.session.add(new_user)
            self.session.commit()
            return True
        except Exception:
            return False

    def get_user_by_email(self, email=None, serialize=False):
        """
        If the email parameter is  provided, the application looks up the user with the provided eamil,
        else it returns None

        :param email: The email of user intended to be searched
        :return: The user with the matching username or email.
        """
        single_user = None
        if email:
            single_user = self.session.query(Users).filter_by(email=email).first()

        if serialize and single_user:
            return [user.serialize() for user in single_user]
        else:
            return single_user

    def get_user_by_id(self, user_id=None, serialize=False):
        """
        If the user_id parameter is  provided, the application looks up the user with the provided id,
        else it returns all the users

        :param user_id: The id of the user intended to be searched(default value is None)
        :return: The user with the matching id or all users.
        """

        all_users = []

        if user_id is None:
            all_users = self.session.query(Users).order_by(Users.last_name).all()
        else:
            if int(user_id) < 0:
                return all_users
            else:
                all_users = self.session.query(Users).filter(Users.user_id == user_id).all()

        if serialize:
            return [user.serialize() for user in all_users]
        else:
            return all_users

    def update_user(self, user_id, new_user):
        """
        The application looks up the user with the provided user_id
        in order to update the user's details

        :param user_id: The id of the user intended to be updated
        :param new_user: user object that holds updated details
        :return: The user with the matching id.
        """

        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        updated_user = None
        users = self.get_user_by_id(user_id)
        user = None
        if len(users) is not 1:
            return updated_user
        else:
            user = users[0]

        if user:
            user.email = new_user["email"]
            user.phone = new_user["role"]
            user.first_name = new_user["first_name"]
            user.last_name = new_user["last_name"]
            self.session.add(user)
            self.session.commit()
            updated_user = self.get_user_by_id(user_id)[0]

        return updated_user.serialize()

    def update_password(self, user_id, new_user):
        """
        The application looks up the user with the provided user_id
        in order to update the user's password

        :param user_id: The id of the user intended to be updated
        :param new_user: user object that holds updated details
        :return: The user with the matching id.
        """

        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        updated_user = None
        users = self.get_user_by_id(user_id)
        user = None
        if len(users) is not 1:
            return updated_user
        else:
            user = users[0]

        if user:
            user.email = new_user["password"]
            self.session.add(user)
            self.session.commit()
            updated_user = self.get_user_by_id(user_id)[0]

        return updated_user.serialize()

    def delete_user(self, user_id):
        """
        The application looks up the user with the provided user_id
        in order to delete the user object from the database

        :param user_id: The id of the user intended to be deleted
        :return: True if user object was deleted, else False.
        """
        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        if user_id:
            try:
                user_deleted = self.session.query(Users).filter(Users.user_id == user_id).first()
                self.session.delete(user_deleted)
                self.session.commit()
                return True
            except Exception as ex:
                print(ex)
                return False

    def create_job(self, job_id=None,
                   job_name=None,
                   verbatim=None,
                   timestamp=None,
                   duration=None,
                   description=None):
        """

        The method creates and saves a new job to the database.

        :param job_id: the job id
        :param job_name: the job name
        :param verbatim: set to true if verbatim is required
        :param timestamp: set to true if timestamp is required
        :param duration: duration of job
        :param description: description of job
        :param user: user associated with the job
        :return: The id of the new job
        """

        created_job = Jobs(job_id=job_id,
                           job_name=job_name,
                           verbatim=verbatim,
                           timestamp=timestamp,
                           duration=duration,
                           description=description)
        self.session.add(created_job)
        self.session.commit()

        return created_job.job_id

    def update_rate(self, rate_id, new_rate):
        """
        The application looks up the rate with the provided rate id
        in order to update the rate's details

        :param rate_id: The id of the rate intended to be updated
        :param new_rate: rate object that holds updated details
        :return: The rate with the matching id.
        """

        if int(rate_id) < 0:
            raise ValueError('Parameter [rate_id] should be positive!')

        updated_rate = None
        rates = self.get_rate_by_id(rate_id)
        rate = None
        if len(rates) is not 1:
            return updated_rate
        else:
            rate = rates[0]

        if rate:
            rate.description = new_rate["description"]
            rate.rate = new_rate["rate"]
            self.session.add(rate)
            self.session.commit()
            updated_rate = self.get_rate_by_id(rate_id)[0]

        return updated_rate.serialize()

    def create_rate(self, rate=None, description=None):
        """

        The method creates and saves a new rate to the database.

        :param rate: all job rate
        :param description: description of rate
        :return: The id of the new rate
        """

        created_rate = Rate(rate=rate, description=description)
        self.session.add(created_rate)
        self.session.commit()

        return created_rate.rate_id

    def get_rate_by_id(self, rate_id=None, serialize=False):
        """
        If the rate_id parameter is  provided, the application looks up the rate with the provided id,
        else it returns all the rates

        :param rate_id: The id of the rate intended to be searched(default value is None)
        :return: The user with the matching id or all users.
        """

        all_rates = []

        if rate_id:
            all_rates = self.session.query(Rate).filter(Rate.rate_id == rate_id).all()
        elif rate_id is None:
            all_rates = self.session.query(Rate).order_by(Rate.rate_id).all()

        if serialize:
            return [rate.serialize() for rate in all_rates]
        else:
            return all_rates

    def update_job(self, job_id, new_job):
        """
        The application looks up the job with the provided job_id
        in order to update the job's details

        :param job_id: The id of the job intended to be updated
        :param new_job: job object that holds updated details
        :return: The job with the matching id.
        """

        updated_job = None
        jobs = self.get_job_by_id(job_id)
        job = None
        if len(jobs) is not 1:
            return updated_job
        else:
            job = jobs[0]

        if job:
            job.date_completed = new_job["date_completed"]
            job.competed = new_job["competed"]
            job.verbatim = new_job["verbatim"]
            job.timestamp = new_job["timestamp"]
            job.duration = new_job["duration"]
            job.description = new_job["description"]
            self.session.add(job)
            self.session.commit()
            updated_job = self.get_job_by_id(job_id)[0]

        return updated_job.serialize()

    def get_job_by_id(self, job_id=None, serialize=False):
        """
        If the job_id parameter is  provided, the application looks up the job with the provided id,
        else it returns all the jobs

        :param job_id: The id of the job intended to be searched(default value is None)
        :return: The job with the matching id or all jobs.
        """

        all_jobs = []

        if job_id is None:
            all_jobs = self.session.query(Jobs).order_by(Jobs.job_id).all()
        else:
            all_jobs = self.session.query(Jobs).filter(Jobs.job_id == job_id).all()

        if serialize:
            return [job.serialize() for job in all_jobs]
        else:
            return all_jobs

    def get_item_by_id(self, item_id=None, serialize=False):
        """
        If the item_id parameter is  provided, the application looks up the job with the provided id,
        else it returns all the jobs

        :param item_id: The id of the item intended to be searched(default value is None)
        :return: The job with the matching id or all jobs.
        """

        all_jobs = []

        if item_id is None:
            all_jobs = self.session.query(JobsDetails).order_by(JobsDetails.job_details_id).all()
        else:
            if int(item_id) < 0:
                return all_jobs
            else:
                all_jobs = self.session.query(JobsDetails).filter(JobsDetails.job_details_id == item_id).all()

        if serialize:
            return [job.serialize() for job in all_jobs]
        else:
            return all_jobs

    def get_user_job_by_id(self, job_id=None, user=None, serialize=False):
        """
        If the job_id parameter is  provided, the application looks up the job with the provided id,
        else it returns all the jobs

        :param job_id: The id of the job intended to be searched(default value is None)
        :param user: user assigned to the job
        :return: The job with the matching id or all jobs.
        """

        all_jobs = []

        if job_id is None:
            all_jobs = self.session.query(Jobs).filter(Jobs.user == user).order_by(Jobs.job_id).all()
        else:
            if int(job_id) < 0:
                return all_jobs
            else:
                all_jobs = self.session.query(Jobs).filter(Jobs.job_id == job_id) \
                    .filter(Jobs.user == user).all()

        if serialize:
            return [job.serialize() for job in all_jobs]
        else:
            return all_jobs

    def delete_job(self, job_id):
        """
        The application looks up the job with the provided job id
        in order to delete the job object from the database

        :param job_id: The id of the job intended to be deleted
        :return: True if job object was deleted, else False.
        """

        if job_id:
            try:
                job_list = self.session.query(Jobs).filter(Jobs.job_id == job_id).first()
                self.session.delete(job_list)
                self.session.commit()
                return True
            except Exception as ex:
                return False

    def user_login_authentication(self, email=None, password=None):
        """
        The method checks for username/email and password match in the database

        :param email: authentication email
        :param password: authentication password
        :return: dictionary of authentication status
        """
        if email and password:
            user = self.get_user_by_email(email=email)
            if user and user.check_user_password(password):
                return {'status': True, 'User': user}
            else:
                return {'status': False, 'User': None}
        else:
            return {'status': False, 'User': None}

    def populate_database(self):

        #
        # Users
        #

        user1 = Users(first_name='kevin',
                      last_name='khanyereri',
                      email='keugeneliyai@gmail.com',
                      password='x0bbxdex1c',
                      role='ROLE_ADMIN')

        user2 = Users(first_name='eugene',
                      last_name='liyai',
                      email='keugeneliyai@yahoo.com',
                      password='password',
                      role='ROLE_AGENT')

        self.session.add(user1)
        self.session.add(user2)
        self.session.commit()

        #
        # User's jobs
        #

        job1 = Jobs(job_id='010JSG18DYE3',
                    job_name='First test job',
                    verbatim=None,
                    timestamp=None,
                    duration=30,
                    description='first job give to one person')

        job2 = Jobs(job_id='0104SG1SDYE3',
                    job_name='Second test job',
                    verbatim=None,
                    timestamp=True,
                    duration=10,
                    description='From 0min to 10min')

        job3 = Jobs(job_id='010DOISDU733',
                    job_name='Third test job',
                    verbatim=True,
                    timestamp=True,
                    duration=50,
                    description='From 0min to 50min')

        job4 = Jobs(job_id='01032DISDU733',
                    job_name='fOURTH test job',
                    verbatim=True,
                    timestamp=True,
                    duration=50,
                    description='From 0min to 50min')

        job5 = Jobs(job_id='KSFFU9EHDU998',
                    job_name='Third test job',
                    verbatim=True,
                    timestamp=False,
                    duration=18,
                    description='From 0min to 18min')

        self.session.add(job1)
        self.session.add(job2)
        self.session.add(job3)
        self.session.add(job4)
        self.session.add(job5)
        self.session.commit()

        #
        # Job Details
        #

        job_details1 =JobsDetails(duration=30,
                                  job_name=job4.job_name,
                                  description='from min 10 to min 40',
                                  user=user1.user_id,
                                  job=job4.job_id)

        job_details2 = JobsDetails(duration=10,
                                   job_name=job2.job_name,
                                   description='whole file',
                                   user=user1.user_id,
                                   job=job2.job_id)

        job_details3 = JobsDetails(duration=10,
                                   job_name=job4.job_name,
                                   description='from min 40 to min 50',
                                   user=user2.user_id,
                                   job=job4.job_id)

        job_details4 = JobsDetails(duration=10,
                                   job_name=job4.job_name,
                                   description='from min 0 to min 10',
                                   user=user2.user_id,
                                   job=job4.job_id)

        job_details5 = JobsDetails(duration=30,
                                   job_name=job1.job_name,
                                   description='whole file',
                                   user=user2.user_id,
                                   job=job1.job_id)

        job_details6 = JobsDetails(duration=5,
                                   job_name=job3.job_name,
                                   description='0 to 5 min',
                                   user=user2.user_id,
                                   job=job3.job_id)

        job_details7 = JobsDetails(duration=5,
                                   job_name=job3.job_name,
                                   description='5 to 10 min',
                                   user=user2.user_id,
                                   job=job3.job_id)

        job_details8 = JobsDetails(duration=5,
                                   job_name=job3.job_name,
                                   description='10 to 15 min',
                                   user=user2.user_id,
                                   job=job3.job_id)

        job_details9 = JobsDetails(duration=5,
                                   job_name=job3.job_name,
                                   description='15 to 20 min',
                                   user=user2.user_id,
                                   job=job3.job_id)

        job_details10 = JobsDetails(duration=10,
                                    job_name=job3.job_name,
                                    description='20 to 30 min',
                                    user=user2.user_id,
                                    job=job3.job_id)

        job_details11 = JobsDetails(duration=10,
                                    job_name=job3.job_name,
                                    description='30 to 40 min',
                                    user=user2.user_id,
                                    job=job3.job_id)

        job_details12 = JobsDetails(duration=5,
                                    job_name=job3.job_name,
                                    description='40 to 45 min',
                                    user=user2.user_id,
                                    job=job3.job_id)

        job_details13 = JobsDetails(duration=5,
                                    job_name=job3.job_name,
                                    description='45 to 50 min',
                                    user=user2.user_id,
                                    job=job3.job_id)

        job_details14 = JobsDetails(duration=18,
                                    job_name=job5.job_name,
                                    description='whole file',
                                    user=user2.user_id,
                                    job=job5.job_id)

        self.session.add(job_details1)
        self.session.add(job_details2)
        self.session.add(job_details3)
        self.session.add(job_details4)
        self.session.add(job_details5)
        self.session.add(job_details6)
        self.session.add(job_details7)
        self.session.add(job_details8)
        self.session.add(job_details9)
        self.session.add(job_details10)
        self.session.add(job_details11)
        self.session.add(job_details12)
        self.session.add(job_details13)
        self.session.add(job_details14)
        self.session.commit()

        #
        # Job rates
        #

        rate = Rate(rate=20, description='Initial rates')
        self.session.add(rate)
        self.session.commit()

        return 'Database Populated'
