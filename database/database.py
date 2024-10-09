from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from .models import Base, Activity
from config import Config


class Database:
    def __init__(self, db_name=Config["STRAVA"].get("database")):
        # Initialize the SQLite3 database connection
        self.engine = create_engine(f"sqlite:///{db_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.tmp = None

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

    def get_latest_activity(self):
        session = self.Session()
        latest_activity = (
            session.query(Activity)
            .order_by(Activity.start_date.desc())
            .offset(0)
            .first()
        )
        session.close()
        if latest_activity:
            print(f"Latest activity: {latest_activity.start_date}")
            return latest_activity.start_date
        else:
            return None

    def get_first_activity(self):
        session = self.Session()
        first_activity = (
            session.query(Activity).order_by(Activity.start_date).offset(0).first()
        )
        session.close()
        if first_activity:
            print(f"First activity: {first_activity.start_date}")
            return first_activity.start_date
        else:
            return None

    def get_activity_count_per_year(
        self,
        compat=False,
        start_year=int(Config["STRAVA"].get("start_year")),
        end_year=int(Config["STRAVA"].get("end_year")),
    ):
        """_summary_

        Args:
            compat (bool, optional): _description_. Defaults to False. Read db file from running_page project
            start_year (int, optional): _description_. Get from config file. 
            end_year (int, optional): _description_. Get from config file.

        Returns:
            _type_: _description_
        """
        # Create a new session
        session = self.Session()

        count_key = "id"
        # Query to count activities grouped by year between start_year and end_year
        result = (
            session.query(
                func.strftime("%Y", Activity.start_date).label("year"),
                func.count(count_key).label("count"),
            )
            .filter(
                func.strftime("%Y", Activity.start_date).between(
                    str(start_year), str(end_year)
                )
            )
            .group_by("year")
            .order_by("year")
            .all()
        )

        # Close the session
        session.close()

        # Print the results
        for year, count in result:
            print(f"Year: {year}, Number of Activities: {count}")

        return result
