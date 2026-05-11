from crewai.tools import tool
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

@tool
def search_nearby_restaurants(location: str, keyword: str = "restaurant") -> str:
    """Search real restaurants near a location using Google Places API."""
    if not GOOGLE_API_KEY:
        return "Google Places API key not configured."

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": f"{keyword} in {location}",
        "key": GOOGLE_API_KEY,
        "rankby": "prominence"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data['status'] != 'OK':
            return f"Error: {data.get('status')} - {data.get('error_message', '')}"

        results = []
        for place in data.get('results', [])[:8]:  # Top 8 restaurants
            results.append({
                "name": place['name'],
                "address": place.get('formatted_address', 'Address not available'),
                "rating": place.get('rating', 'N/A'),
                "total_ratings": place.get('user_ratings_total', 'N/A'),
                "place_id": place['place_id']
            })

        return str(results)

    except Exception as e:
        return f"Error fetching restaurants: {str(e)}"


@tool
def get_restaurant_details(place_id: str) -> str:
    """Get more details of a specific restaurant."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": GOOGLE_API_KEY,
        "fields": "name,formatted_address,rating,formatted_phone_number,opening_hours,price_level"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] == 'OK':
            return str(data['result'])
        return "Details not found"
    except Exception as e:
        return f"Error: {str(e)}"