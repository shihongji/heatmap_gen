import json
import sqlite3
from datetime import datetime

# Connect to your SQLite database
conn = sqlite3.connect("strava_activities.db")
cursor = conn.cursor()

# Fetch activity data, grouped by date (assuming `start_date` is stored as a UTC datetime object)
query = """
    SELECT DATE(start_date) as date, COUNT(*) as activity_count
    FROM activities
    GROUP BY DATE(start_date)
    ORDER BY DATE(start_date);
"""
cursor.execute(query)
results = cursor.fetchall()

# Convert fetched data into the required format for Cal-Heatmap
# { "timestamp": activity_count } -> [{ "date": timestamp, "count": activity_count }]
formatted_data = [{"date": int(datetime.strptime(date, "%Y-%m-%d").timestamp()), "count": count} for date, count in results]

# Save data in the new format to a JSON file
with open("heatmap_data.json", "w") as f:
    json.dump({"data": formatted_data}, f, indent=4)

print("Data has been saved to heatmap_data.json in the required format.")
conn.close()