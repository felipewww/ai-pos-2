import os
from dotenv import load_dotenv
load_dotenv()

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
MATRIX_LIB = os.getenv("MATRIX_LIB") or 'haversine'
