"""
File      : rate.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates rates and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================

from sqlalchemy import Column, Integer, Text

from the_hive.models.db_model import Model


class Rate(Model):
    __tablename__ = 'Rate'
    rate_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rate = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "rate_id": self.rate_id,
            "rate": self.rate,
            "description": self.description
        }
