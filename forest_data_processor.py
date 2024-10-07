import pandas as pd
from datetime import datetime, timedelta
import json
from config import Config

# Load CSV data from a file
file_path = Config['FOREST'].get('import_csv')  
df = pd.read_csv(file_path)

# Convert the 'Start Time' and 'End Time' columns to datetime
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['End Time'] = pd.to_datetime(df['End Time'])

# Ensure that all datetime columns are timezone-aware
df['Start Time'] = df['Start Time'].dt.tz_localize(None)
df['End Time'] = df['End Time'].dt.tz_localize(None)

# Function to split focus time if it spans multiple days
def split_focus_time(start_time, end_time):
    events = []
    
    # Loop until the start time and end time are on the same day
    while start_time.date() != end_time.date():
        # Calculate the time remaining until midnight of the start time's day
        # Ensure end_of_day is tz-aware
        end_of_day = datetime.combine(start_time.date() + timedelta(days=1), datetime.min.time()).replace(tzinfo=start_time.tzinfo)
        focus_seconds = (end_of_day - start_time).total_seconds()
        
        # Create an event for the time until midnight
        events.append((start_time.date(), focus_seconds))
        
        # Update start time to midnight of the next day
        start_time = end_of_day
    
    # Add the remaining time on the same day
    focus_seconds = (end_time - start_time).total_seconds()
    events.append((start_time.date(), focus_seconds))
    
    return events

# Split the focus time for each record that spans multiple days
split_data = []
for _, row in df.iterrows():
    split_data.extend(split_focus_time(row['Start Time'], row['End Time']))

# Create a new DataFrame from the split data
split_df = pd.DataFrame(split_data, columns=['Date', 'Focus (seconds)'])

# Group by day and aggregate the total focus time in seconds
daily_focus = split_df.groupby('Date')['Focus (seconds)'].sum().reset_index()

# Convert date to UNIX timestamp and rename columns as per the required structure
daily_focus['date'] = daily_focus['Date'].apply(lambda x: int(datetime.strptime(str(x), '%Y-%m-%d').timestamp()))
daily_focus['focus'] = (daily_focus['Focus (seconds)'] / 60).astype(int)
# convert to minutes

# Create the structured JSON format
structured_json = {
    "data": daily_focus[['date', 'focus']].to_dict(orient='records')
}

# Save the JSON to a file or print it
output_file = Config['FOREST'].get('export_json')
with open(output_file, 'w') as json_file:
    json.dump(structured_json, json_file, indent=4)
    print(f"Data saved to {output_file}")