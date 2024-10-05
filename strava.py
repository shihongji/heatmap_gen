from dotenv import load_dotenv
import os
import json
import stravalib
from datetime import datetime
from decorators import timeit
from database import Database

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

    @timeit
    def save_activities_to_json(self, activities, filename="activities.json"):
        serializable_activities = []
        
        for activity in activities:
            activity_dict = activity.model_dump(mode='json')
            serializable_activities.append(activity_dict)
            
        with open(filename, "w") as f:
            json.dump(serializable_activities, f, indent=4)
        print(f"Activities saved to {filename}")

    @staticmethod
    def filter_activity_data(activity_dict):
        relevant_fields = {
            'id', 'distance', 'moving_time', 'elapsed_time', 'start_date', 
            'average_speed', 'type', 'max_speed', 'name', 'timezone' 
        }
        return {k: v for k, v in activity_dict.items() if k in relevant_fields}
    
    @timeit
    def save_activities_to_db(self, activities):
        db = Database()
        
        count = 0
        for activity in activities:
            activity_dict = activity.model_dump(mode='json')
            filtered_activity_dict = self.filter_activity_data(activity_dict)
            filtered_activity_dict['start_date'] = datetime.fromisoformat(filtered_activity_dict['start_date'].replace('Z', '+00:00'))
            db.add_activity(filtered_activity_dict)
            count += 1
        
        print(f"{count} activities saved to the database")