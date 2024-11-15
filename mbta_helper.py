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


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode("utf-8")
            data = json.loads(response_text)
            return data
    except Exception as e:
        print(f"Sorry, could not retrieve the json data. Please try a new location.\nError: {e}")
    return {}


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    # Prepare url for the API request (replace space by %20 etc... that can be used in url links)
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


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
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


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
        # Step 1: Get latitude and longitude for the place name
    latitude, longitude = get_lat_lng(place_name)
    if latitude is None or longitude is None:
        print("Could not determine location.")
        return None, None

    # Step 2: Find the nearest station using the coordinates
    station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
    if station_name is None:
        print("No nearby MBTA station found.")
        return None, None

    # Step 3: Return the station name and accessibility status
    return station_name, wheelchair_accessible


def main():
    """
    You should test all the above functions here
    """
    place_name = "Prudential"
    station_name, wheelchair_accessible = find_stop_near(place_name)
    if station_name:
        print(f'Your current location is {place_name}')
        print(f"Nearest MBTA station to {place_name}: {station_name}")
        print(f"Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}")


if __name__ == "__main__":
    main()
