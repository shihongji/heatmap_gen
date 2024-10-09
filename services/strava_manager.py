from services.strava import Strava
from database.database import Database
from typing import Iterator, Optional
from stravalib.model import SummaryActivity


class StravaManager:
    def __init__(self, strava: Strava, db: Database):
        """Initialize with instances of Strava and Database."""
        self.strava = strava
        self.db = db

    def retrieve_new_activities(self) -> Optional[Iterator[SummaryActivity]]:
        """Retrieve new activities from Strava after the latest stored activity."""
        last_time = self.db.get_latest_activity()
        activities = self.strava.get_activities(after=last_time)
        if activities:
            num_activities = self.strava.save_activities_to_db(activities)
            print(f"{num_activities} activities added to the database.")
        return None

    def initial_setup(self) -> None:
        """Setup database with all available activities from Strava."""
        self.db.drop_table()
        activities = self.strava.get_activities()
        self.strava.save_activities_to_db(activities)
        print("Initial setup completed.")

    def check_yearly_activity_count(self) -> None:
        self.db.get_activity_count_per_year()