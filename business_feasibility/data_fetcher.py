import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_nearby_businesses(location, business_type, radius=1000):
    """
    Fetch nearby businesses from Google Places API
    location: "lat,lng"
    business_type: e.g., restaurant, cafe
    radius: in meters
    """
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={business_type}&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(url).json()
        return response.get('results', [])[:10]  # Limit to 10 for free-tier
    except Exception as e:
        print("Failed to fetch Google Places data:", e)
        return []
