from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Activity

class Database:
    def __init__(self, db_name="strava_activities.db"):
        # Initialize the SQLite3 database connection
        self.engine = create_engine(f"sqlite:///{db_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_activity(self, activity_data):
        # Create a new session
        session = self.Session()
        try:
            # Create an Activity object from the data and add it to the session
            activity = Activity(**activity_data)
            session.add(activity)
            session.commit()
            print(f"Activity {activity.name} added to the database.")
        except Exception as e:
            session.rollback()
            print(f"Error adding activity: {e}")
        finally:
            session.close()

    def get_all_activities(self):
        # Retrieve all activities from the database
        session = self.Session()
        activities = session.query(Activity).all()
        session.close()
        return activities
    
    def drop_table(self):
        # Drop the activities table
        Base.metadata.drop_all(self.engine, tables=[Activity.__table__])
        print("Table dropped.")