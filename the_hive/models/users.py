"""
File      : users.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates users and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Numeric, Date, desc
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship

from the_hive.models.db_model import Model


class Users(Model, UserMixin):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    hash_password = Column(String(1000))
    date_added = Column(Date, default=datetime.utcnow)
    date_modified = Column(Date, default=datetime.utcnow)
    role = Column(String(20), nullable=False)
    jobs = relationship('Jobs', backref="Users")

    def get_id(self):
        return self.user_id

    def check_user_password(self, _password):
        return check_password_hash(self.hash_password, _password)

    @property
    def password(self, password):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_added": self.date.isoformat() if self.date_added else "",
            "date_modified": self.date.isoformat() if self.date_modified else "",
            "role": self.role,
            "jobs": [job.serialize() for job in self.jobs]
        }