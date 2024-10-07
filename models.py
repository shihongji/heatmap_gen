from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for all the models
Base = declarative_base()

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    timezone = Column(String)
    distance = Column(Float)
    average_speed = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    type = Column(String)
    max_speed = Column(Float)

    def __repr__(self):
        return f"<Activity(name={self.name}, start_date={self.start_date}, type={self.type}, distance={self.distance})>"
