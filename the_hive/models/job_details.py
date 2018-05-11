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

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text

from the_hive.models.db_model import Model


class JobsDetails(Model):
    __tablename__ = 'JobsDetails'
    job_details_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    job_name = Column(String(100))
    paid = Column(Boolean, default=False, nullable=False)
    date_created = Column(Date, default=datetime.utcnow)
    date_completed = Column(Date)
    competed = Column(Boolean, default=False, nullable=False)
    duration = Column(Integer, nullable=False)
    download_link = Column(String(255), nullable=False)
    description = Column(Text)
    user = Column(Integer, ForeignKey('Users.user_id'))
    job = Column(String(100), ForeignKey('Jobs.job_id'))

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "job_details_id": self.job_details_id,
            "name": self.job_name,
            "competed": self.competed,
            "duration": self.duration,
            "paid": self.paid,
            "description": self.description,
            "date_created": self.date_created.isoformat() if self.date_created else "",
            "date_completed": self.date_completed.isoformat() if self.date_completed else "",
            "link": self.download_link,
            "user": self.user,
            "job": self.job
        }
