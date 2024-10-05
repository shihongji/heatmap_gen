from strava import Strava

# Example usage:
if __name__ == "__main__":
    strava = Strava()
    activities = strava.get_activities()
    strava.save_activities_to_json(activities)

