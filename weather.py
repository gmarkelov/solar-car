"""
This script requests forecast from OpenWeather for next 5 days with 3 hour steps for multiple cities and stores 
the data(date, tempreture and description such as rain/cloudy/clear sky) in json files that are being created in 
the same directory as the script.
"""
import requests
import os
import json
from datetime import datetime

# API key set through terminal in OS environment in terminal
API_KEY = os.environ.get('API_KEY')

cities = [
    {"city": "Darwin"},
    {"city": "Sydney"},
    {"city": "Perth"},
    {"city": "Adelaide"}
]
country = "AU"


# Loop through each city to get the forecats data
for location in cities:
    city = location["city"]

    # URL for the 5-day / 3-hour forecast API
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    forecast_data = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        # Create a list to store the forecast data
        data_to_store = []

        # Loop through the forecast for every 3 hours
        for forecast in forecast_data['list']:
            # Get the datetime of the forecast
            dt = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']

            # Append each forecast as a dictionary to the list
            data_to_store.append({
                "datetime": dt,
                "temperature": temp,
                "description": description
            })

        # Save the list as a JSON file
        with open(f"{city}_forecast.json", 'w') as json_file:
            json.dump(data_to_store, json_file, indent=4)

        print(f"Forecast data saved to {city}_forecast.json")
    else:
        # Handle errors
        print(f"Error fetching data for {city}: {forecast_data['message']}")