# Activity Heatmap Generator

This project helps you generate heatmaps for visualizing your activities. See a [Live Demo](https://hire.hongji.me/#my-heatmap).

## Supported Data Sources

- **Exercise Data**: Strava activities fetched via the Strava API (requires configuration of account tokens).
- **Focus Time**: Focused time data exported as CSV from the Forest App.

## How It Works

### For Strava Data
1. Retrieve data from the Strava API.
2. Process and store it in the SQLite database.
3. Export processed data to JSON format.

### For Focus Time Data
1. Export the CSV file from the Forest App.
2. Process the CSV and convert it into JSON format.

### Heatmap Visualization
The JavaScript library `Heat.js` loads the generated JSON data to create interactive heatmaps.

## Prerequisites

1. **Install the required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

2.	Set up the following configuration files:
	•	config.ini: Configure your data file paths.
	•	.env: Set up your Strava API tokens.
3.	Export JSON data using the provided scripts.

## Requirements

The required Python packages for this project are listed in requirements.txt. Make sure to install them before running the project:

pandas
requests
sqlalchemy
python-dotenv

## How to Use

1.	Configure your settings:
    - Define data file paths in config.ini.
	-	Set up Strava tokens in the .env file.
2.	Generate JSON files:
	-	Run the Python scripts to fetch and process the data.
	-	Export the processed data into JSON format.
3.	Visualize:
	-	Use the React project in the heatmap folder to render the heatmaps with the generated JSON data.

## Next Steps

1.	React Integration: The current implementation of Heat.js in React is basic. Further development is needed to make it more generalized and modular.
2.	Data Processing Pipeline: Improve the data processing flow for a more streamlined and automated pipeline.
3.	Additional Data Sources: Support more data categories, such as GitHub contributions and other fitness tracking apps.

## Inspiration

This project is inspired by [yihong0618/running_page](https://github.com/yihong0618/running_page), which helps a lot of runners creating their personal running pages.

## Acknowledgements

- Heatmap visualization is powered by [Heat.js - JavaScript Heat Map](https://www.william-troup.com/heat-js/).
