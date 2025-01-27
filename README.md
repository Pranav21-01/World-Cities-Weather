# World-Cities-Weather
This project retrieves current weather data for a list of cities using the OpenWeatherMap and Google Geocoding APIs. The data includes temperature, humidity, and weather description, which is then visualized in a bar chart. The project also highlights the cities with the highest and lowest temperatures.


## Setup Instructions
1. Clone the repository or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Update config.json: 
    Replace the placeholders in config.json with the API keys for Google's Geocoding API and OpenWeather Current Weather API. For example:-
   
    {
    "GOOGLE_API_KEY": "your-google-api-key",
    "OPENWEATHER_API_KEY": "your-openweather-api-key"
    }

   
4. Run the Script:
    ```bash
    python main.py
