import json
import sqlite3
from datetime import datetime
from config import Config

# Connect to your SQLite database
conn = sqlite3.connect(Config["STRAVA"].get("database"))
cursor = conn.cursor()

# Fetch activity data, grouped by date (assuming `start_date` is stored as a UTC datetime object)
query = """
    SELECT DATE(start_date_local) as date, SUM(distance) as total_distance
    FROM activities
    GROUP BY DATE(start_date_local)
    ORDER BY DATE(start_date_local);
"""
cursor.execute(query)
results = cursor.fetchall()

# Convert fetched data into the required format for Cal-Heatmap
# { "timestamp": activity_count } -> [{ "date": timestamp, "count": activity_count }]
formatted_data = [{"date": int(datetime.strptime(date, "%Y-%m-%d").timestamp()), "distance": round(total_distance)} for date, total_distance in results]

# Save data in the new format to a JSON file
file_name = Config["STRAVA"].get("export_json")
with open(file_name, "w") as f:
    json.dump({"data": formatted_data}, f, indent=4)

print(f"Data saved to {file_name}")
conn.close()