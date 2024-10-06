from strava import Strava
from database import Database
from datetime import datetime
from typing import Optional, Iterator
from stravalib.model import SummaryActivity

def drop_table():
    db = Database()
    db.drop_table()

def check_db():
    db = Database()
    activities = db.get_all_activities()
    for activity in activities[:10]:
        print(activity)

def retrieve_new_activities() -> Iterator[SummaryActivity]:
    strava = Strava()
    db = Database()
    last_time: Optional[datetime] = db.get_latest_activity()
    activities: Optional[Iterator[SummaryActivity]] = strava.get_activities(after=last_time) 
    return activities

def initial_setup():
    db = Database()
    db.drop_table()
    strava = Strava()
    activities = strava.get_activities()
    strava.save_activities_to_db(activities)

def check_first_activity():
    db = Database()
    first_activity = db.get_first_activity()
    print(first_activity) 
    db.get_activity_count_per_year()
# Example usage:
if __name__ == "__main__":
    # strava.save_activities_to_db(activities)
    # check_db()
    # initial_setup()
    check_first_activity()
    

