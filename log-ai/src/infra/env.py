import os
from dotenv import load_dotenv
load_dotenv()

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
