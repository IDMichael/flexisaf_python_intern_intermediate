# Weather API Application - API Authentication & Error Handling Upgrade

## Overview

This Python application retrieves real-time weather information using the OpenWeatherMap API.

This project is an upgraded version of the original Weather API Application. The upgrade focuses on improving API authentication, configuration management, and error handling to create a more reliable and user-friendly application.

The application:
- Accepts a city name from the user
- Sends authenticated requests to the OpenWeatherMap API
- Retrieves current weather information
- Displays formatted weather reports
- Handles API authentication failures
- Handles API rate limits
- Handles invalid city requests
- Handles network and timeout errors
- Uses environment variables for secure API configuration

# Features

## API Authentication
- Uses an OpenWeatherMap API key securely through environment variables
- Prevents storing sensitive credentials directly inside source code
- Validates API configuration before running the application


## Error Handling
The application handles different types of failures, including:
- Missing API key
- Invalid API key (`401 Unauthorized`)
- Invalid city name (`404 Not Found`)
- API rate limit exceeded (`429 Too Many Requests`)
- Weather service unavailable (`500+ Server Errors`)
- Network connection failures
- Request timeout errors
- Invalid API responses


## Application Features
- Real-time weather information retrieval
- City input validation
- Clean weather report formatting
- Modular project structure
- Separation of responsibilities between files
- Secure environment configuration

# Technologies Used
- Python 3
- OpenWeatherMap API
- Requests Library
- Python-dotenv

# Required Libraries
requests==2.32.5
python-dotenv==1.1.1

## Environment Configuration
Create a `.env` file in the project folder and add your OpenWeather API credentials:

Replace `YOUR_API_KEY` with your actual OpenWeather API key.

## How to Run the Program
### 1. Navigate into the folder
cd weather_api_app_upgrade

### 2. Install required dependencies
pip install -r requirements.txt

### 3. Run the program
python main.py