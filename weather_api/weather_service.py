import requests
from config import (API_KEY, BASE_URL, UNITS, LANGUAGE, REQUEST_TIMEOUT)

# Handles communication with the weather API
def get_weather(city):

	# Remove extra spaces
	city = city.strip()

	# Check if city name is empty
	if not city:
		return {
		"success": False,
		"message": "City name cannot be empty."}

	# API request parameters
	params = {
		"q": city,
		"appid": API_KEY,
		"units": UNITS,
		"lang": LANGUAGE
	}

	try:
		# Send request to the API
		response = requests.get(
				BASE_URL,
				params=params,
				timeout=REQUEST_TIMEOUT
				)
	
		# Convert the response to JSON
		try:
			data = response.json()
		except ValueError:
			return {
				"success": False,
				"message": "Invalid response received from weather service."
			}
		# Invalid API key
		if response.status_code == 401:
			return {
				"success": False,
				"message": "Invalid API key."				
			}

		# City not found
		if response.status_code == 404:
			return {
				"success": False,
				"message": "City not found."
			}

		# Any other API error
		if response.status_code != 200:
			return {
				"success": False,
				"message": data.get(
					"message", "Unable to retrieve weather information."
					)
			}

		# Extract only the needed information 
		weather = {
			"city": data["name"],
			"country": data["sys"]["country"],
			"temperature": data["main"]["temp"],
			"feels_like": data["main"]["feels_like"],
			"humidity": data["main"]["humidity"],
			"pressure": data["main"]["pressure"],
			"wind_speed": data["wind"]["speed"],
			"description": data["weather"][0]["description"]
		}

		return {
			"success": True,
			"data": weather
		}

	except requests.exceptions.Timeout:
		return {
			"success": False,
			"message": "Request timed out. Please, try again."
		}
		
	except requests.exceptions.RequestException:
		return {
			"success": False,
			"message": "An unexpected network error occurred."
		}