import os
from dotenv import load_dotenv
import urllib.request
import json

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
    """
    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode("utf-8")
            data = json.loads(response_text)
            return data
    except Exception as e:
        print(f"Could not retrieve the JSON data. Error: {e}")
    return {}

def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.
    """
    # Prepare the URL for the API request
    encoded_place_name = urllib.parse.quote(place_name)
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={encoded_place_name}&access_token={MAPBOX_TOKEN}"

    # Get JSON response
    response_data = get_json(url)

    # Check if we have results and extract coordinates
    location_info = response_data.get("features")
    if location_info:
        coordinates = location_info[0]["geometry"]["coordinates"]
        longitude, latitude = coordinates[0], coordinates[1]
        return str(latitude), str(longitude)
    else:
        print("Location not found.")
        return None, None

def test_get_lat_lng():
    """
    Test the get_lat_lng function with the place name "Boston".
    """
    place_name = "Boston"
    latitude, longitude = get_lat_lng(place_name)
    if latitude and longitude:
        print(f"Coordinates of {place_name}: Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Location not found or an error occurred.")

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.
    """
    # Update MBTA URL with the retrieved coordinates
    MBTA_url = f"{MBTA_BASE_URL}?sort=distance&filter[latitude]={latitude}&filter[longitude]={longitude}"
   
    # Get JSON response
    response_data = get_json(MBTA_url)

    # Check if we have results and extract the necessary information
    stops = response_data.get("data")
    if stops:
        # Access the first stop (nearest stop) details
        station_info = stops[0]
        station_name = station_info["attributes"]["name"]
        wheelchair_accessible = station_info["attributes"]["wheelchair_boarding"] == 1  # 1 indicates wheelchair accessible
        return station_name, wheelchair_accessible
    else:
        print("No station found.")
        return None, None


def test_get_nearest_station():
    """
    Test the get_nearest_station function using coordinates for Boston.
    """
    # Coordinates of Boston (from previous test)
    latitude, longitude = get_lat_lng("Boston")
    
    if latitude and longitude:
        station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
        if station_name:
            print(f"Nearest MBTA station to Boston: {station_name}")
            print(f"Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}")
        else:
            print("No nearby MBTA station found.")
    else:
        print("Location not found or an error occurred.")

# Run the tests
if __name__ == "__main__":
    test_get_lat_lng()
    test_get_nearest_station()

