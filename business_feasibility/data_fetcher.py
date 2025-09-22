import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_nearby_businesses(location, business_type, radius=1000):
    """
    Fetch nearby businesses from Google Places API
    location: "lat,lng"
    business_type: e.g., restaurant, cafe
    radius: in meters
    """
    try:
        lat, lng = location.split(',')
        lat, lng = float(lat), float(lng)
        
        # Use Google Places API to find nearby businesses
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=radius,
            type=business_type
        )
        
        businesses = []
        for place in places_result.get('results', [])[:10]:  # Limit to 10
            business = {
                'name': place.get('name', 'Unknown'),
                'lat': place['geometry']['location']['lat'],
                'lng': place['geometry']['location']['lng'],
                'types': place.get('types', []),
                'rating': place.get('rating', 0),
                'price_level': place.get('price_level', 0),
                'vicinity': place.get('vicinity', ''),
                'place_id': place.get('place_id', '')
            }
            businesses.append(business)
        
        print(f"Found {len(businesses)} businesses for {business_type} near {location}")
        for biz in businesses:
            print(f"- {biz['name']} ({biz.get('rating', 'N/A')} stars)")
        
        return businesses
        
    except Exception as e:
        print(f"Failed to fetch Google Places data: {e}")
        return []

def get_business_details(place_id):
    """
    Get detailed information about a specific business
    """
    try:
        place_details = gmaps.place(
            place_id=place_id,
            fields=['name', 'formatted_phone_number', 'website', 'opening_hours', 'reviews', 'rating', 'user_ratings_total']
        )
        return place_details.get('result', {})
    except Exception as e:
        print(f"Failed to fetch business details: {e}")
        return {}
