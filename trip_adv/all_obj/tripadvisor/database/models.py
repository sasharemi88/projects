from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Numeric, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_first_day_of_quarter(date: datetime):
    return datetime(date.year, 3*((date.month-1)//3)+1, 1)


class LocationObject(Base):
    __tablename__ = 'locations'

    object_id = Column(Integer, primary_key=True)
    location_id = Column(Integer)
    name = Column(String, nullable=False)
    address = Column(String)
    category = Column(String)
    subcategory = Column(String)
    subtype_cat = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    date_create = Column(DateTime, default=datetime.now())
    date_update = Column(DateTime,
                         default=get_first_day_of_quarter(datetime.now()),
                         onupdate=get_first_day_of_quarter(datetime.now()))
