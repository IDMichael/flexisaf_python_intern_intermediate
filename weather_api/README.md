# Weather API Application

## Overview
This Python program retrieves and displays real-time weather information using the OpenWeather API.

The program:
- Accepts a city name from the user
- Sends requests to a weather API service
- Retrieves current weather information
- Displays formatted weather reports
- Handles API errors and network failures
- Uses environment variables for secure API configuration

## Features
- Weather data retrieval using API requests
- Secure API key management with `.env`
- Environment variable loading
- City name validation
- API response validation
- Error handling for invalid keys and missing cities
- Network timeout handling
- Clean weather report display
- Modular file organization

## Technologies Used
- Python 3
- OpenWeather API

## Required Libraries
The program requires the following external libraries:
- `requests`
- `python-dotenv`

## Environment Configuration
Create a `.env` file in the project folder and add your OpenWeather API credentials:

Replace `YOUR_API_KEY` with your actual OpenWeather API key.

## How to Run the Program
### 1. Navigate into the folder
cd weather_api

### 2. Install required dependencies
pip install -r requirements.txt

### 3. Run the program
python main.py