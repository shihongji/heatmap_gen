from dotenv import load_dotenv
import os
import stravalib
from decorators import timeit

load_dotenv()
class Strava:
    def __init__(self):
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.access_token = None
        self.client = stravalib.Client()

        # Get access token
        self.check_access()

    @timeit
    def check_access(self):
        response = self.client.refresh_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.refresh_token,
        )
        # Update the authdata object
        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]

        self.client.access_token = response["access_token"]
        print("Access ok")

    @timeit
    def get_activities(self, **kwargs):
        activities = self.client.get_activities(limit=5)
        return activities
