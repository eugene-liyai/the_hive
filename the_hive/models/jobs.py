"""
File      : jobs.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates jobs and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from datetime import datetime

from sqlalchemy import Column, String, Integer, Date, Boolean, Text
from sqlalchemy.orm import relationship

from the_hive.models.db_model import Model


class Jobs(Model):
    __tablename__ = 'Jobs'
    job_id = Column(String, primary_key=True, nullable=False)
    job_name = Column(String(100), nullable=False)
    date_created = Column(Date, default=datetime.utcnow)
    date_completed = Column(Date)
    competed = Column(Boolean, default=False, nullable=False)
    verbatim = Column(Boolean, default=False, nullable=False)
    timestamp = Column(Boolean, default=False, nullable=False)
    paid = Column(Boolean, default=False, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text)
    user = relationship("Users", backref="Jobs")

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
