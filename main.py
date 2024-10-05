from strava import Strava
from database import Database

def drop_table():
    db = Database()
    db.drop_table()
    
def check_db():
    db = Database()
    activities = db.get_all_activities()
    for activity in activities:
        print(activity)

# Example usage:
if __name__ == "__main__":
    # drop_table()
    strava = Strava()
    activities = strava.get_activities()
    strava.save_activities_to_json(activities)
    strava.save_activities_to_db(activities)
    check_db()
    # check_db()
    
    

