import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Read configuration values
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
UNITS = os.getenv("UNITS", "metric")
LANGUAGE = os.getenv("LANGUAGE", "en")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

# Validate API_KEY and the BASE_URL
def validate_config():
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        raise ValueError("Invalid API_KEY. Please, add your OpenWeatherMap API key to the .env file.")
    
    if not BASE_URL:
        raise ValueError("BASE_URL is missing from the .env file.")