import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Configurations variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Validate API_KEY and the BASE_URL
if not API_KEY:
    raise ValueError("API_KEY is missing from environment variables.")

if not BASE_URL:
    raise ValueError("BASE_URL is missing from environment variables.")

# Units
UNITS = "metric"

# Language for the weather description
LANGUAGE = "en"

# Timeout (in seconds) for API requests
REQUEST_TIMEOUT = 10