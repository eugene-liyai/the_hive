"""
File      : jobs_details.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates job details and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, Text

from the_hive.models.db_model import Model


class JobsDetails(Model):
    __tablename__ = 'JobsDetails'
    job_details_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_created = Column(Date, default=datetime.utcnow)
    date_completed = Column(Date)
    competed = Column(Boolean, default=False, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text)
    user = Column(Integer, ForeignKey('Users.user_id'))
    job = Column(Integer, ForeignKey('Jobs.job_id'))

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "job_id": self.job_id,
            "job_name": self.job_name,
            "competed": self.competed,
            "verbatim": self.verbatim,
            "timestamp": self.timestamp,
            "paid": self.paid,
            "duration": self.duration,
            "description": self.description,
            "date_created": self.date.isoformat() if self.date_created else "",
            "date_completed": self.date.isoformat() if self.date_completed else "",
            "user": self.user
        }
