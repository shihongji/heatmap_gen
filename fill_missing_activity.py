from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Activity
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from datetime import datetime, timedelta

# This script will compare the activities in two databases and store the missing entries in a new table in the second database.

# Define the base class for all the models
Base = declarative_base()

# Connect to both databases
engine_a = create_engine('sqlite:///strava_activities.db')  # DB A
engine_b = create_engine('sqlite:///strava_activities.db')  # DB B

# Create sessions for both databases
SessionA = sessionmaker(bind=engine_a)
SessionB = sessionmaker(bind=engine_b)

# Define a new table in DB B to store the missing entries
class MissingActivity(Base):
    __tablename__ = 'missing_activities'

    run_id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    distance = Column(Float)
    average_speed = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    type = Column(String)
    start_date_local = Column(String)
    location_country = Column(String)
    summary_polyline = Column(String)
    average_heartrate = Column(Float)

    def __repr__(self):
        return f"<MissingActivity(name={self.name}, start_date={self.start_date}, type={self.type}, distance={self.distance})>"

class OriginActivity(Base):
    __tablename__ = 'activities'

    run_id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    distance = Column(Float)
    average_speed = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    type = Column(String)
    start_date_local = Column(String)
    location_country = Column(String)
    summary_polyline = Column(String)
    average_heartrate = Column(Float)

    def __repr__(self):
        return f"<MissingActivity(name={self.name}, start_date={self.start_date}, type={self.type}, distance={self.distance})>"
# Create the new table in DB B
# Base.metadata.create_all(engine_b)

# Function to find and store missing entries
def find_and_store_missing_activities():
    session_a = SessionA()
    session_b = SessionB()

    # Get all entries from DB A (ActivityCompat)
    activities_in_a = session_a.query(OriginActivity).all()

    # Iterate over activities in DB A and check if they exist in DB B
    for activity in activities_in_a:
        # Check if the activity (identified by run_id or start_date) exists in DB B
        exists_in_b = session_b.query(
            exists().where(Activity.start_date == activity.start_date)
        ).scalar()

        # If it doesn't exist in DB B, add it to the new table
        if not exists_in_b:
            # Create a new MissingActivity object
            missing_activity = MissingActivity(
                run_id=activity.run_id,
                name=activity.name,
                start_date=activity.start_date,
                distance=activity.distance,
                average_speed=activity.average_speed,
                moving_time=activity.moving_time,
                elapsed_time=activity.elapsed_time,
                type=activity.type,
                start_date_local=activity.start_date_local,
                location_country=activity.location_country,
                summary_polyline=activity.summary_polyline,
                average_heartrate=activity.average_heartrate,
            )

            # Add to session and commit to DB B
            session_b.add(missing_activity)
            session_b.commit()
            print(f"Added missing activity: {activity.name}, {activity.start_date}")

    # Close both sessions
    session_a.close()
    session_b.close()

# Run the function to find and store missing activities
# find_and_store_missing_activities()
# Utility function to convert datetime to seconds since start date
def convert_to_seconds(start_date, time_value):
    """
    Convert a datetime string to seconds based on the difference from the start date.
    If time_value is a string in the format '1970-01-01 00:25:14.000000', convert it to datetime first.
    """
    if not time_value or not isinstance(time_value, str):
        return None

    try:
        # Convert the time_value string to a datetime object
        time_value_dt = datetime.strptime(time_value, "%Y-%m-%d %H:%M:%S.%f")

        # Calculate the time difference in seconds
        delta = time_value_dt - datetime(1970, 1, 1)
        return int(delta.total_seconds())
    except ValueError:
        print(f"Unable to parse time_value: {time_value}")
        return None
def test():
    session_a = SessionA()
    session_b = SessionB()
    activities_compat = session_a.query(MissingActivity).all()
    for activity in activities_compat:
        new_activity = Activity(
            id=activity.run_id,
            name=activity.name,
            start_date=activity.start_date,
            distance=round(activity.distance, 3),
            timezone="(GMT+08:00) Asia/Shanghai" if activity.location_country[-2:] == "中国" else "(GMT-08:00) America/Los_Angeles",
            average_speed=round(activity.average_speed, 3),
            type=activity.type,
            max_speed=round(activity.average_speed, 3),
            moving_time=convert_to_seconds(activity.start_date, activity.moving_time),
            elapsed_time=convert_to_seconds(activity.start_date, activity.elapsed_time),
        )
        if new_activity.timezone == "(GMT+08:00) Asia/Shanghai":
            # add 8 hours to start_date
            new_activity.start_date = new_activity.start_date + timedelta(hours=8)
        else:
            # subtract 8 hours from start_date
            new_activity.start_date = new_activity.start_date - timedelta(hours=8)
        # add the new activity to DB B if not already present
        exists_in_b = session_b.query(
            exists().where(Activity.id == new_activity.id)
        ).scalar() 
        if exists_in_b:
            print(f"Activity {new_activity.name} already exists in DB B.")
            continue
        session_b.add(new_activity)
        session_b.commit()
    # Close the sessions
    session_a.close()
    session_b.close()

test()