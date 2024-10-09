from services import Strava, StravaManager
from database import Database
from datetime import datetime
from typing import Optional, Iterator
from stravalib.model import SummaryActivity



if __name__ == "__main__":
    strava = Strava()
    db = Database()
    manager = StravaManager(strava, db)
    manager.retrieve_new_activities()
    manager.check_yearly_activity_count()