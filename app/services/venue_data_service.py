import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
from requests.exceptions import RequestException, HTTPError
from app.models.schemas import VenueData, Coordinates
from app.exceptions.exceptions import VenueDataServiceError

load_dotenv()

API_BASE_URL = os.getenv("HOME_ASSIGNMENT_API_BASE_URL")

if not API_BASE_URL:
    raise ValueError("HOME_ASSIGNMENNT_API_BASE_URL environment variable is not set")

def build_static_venue_url(venue_slug: str) -> str:
    return f"{API_BASE_URL}/{venue_slug}/static"

def build_dynamic_venue_url(venue_slug: str) -> str:
    return f"{API_BASE_URL}/{venue_slug}/dynamic"

def handle_http_error(response):
    try:
        error_message = response.json().get("message", "No error message provided")
    except ValueError:
        error_message = response.text
    
    raise HTTPException(
        status_code=response.status_code,
        detail=f"HTTP error occurred: {error_message}",
    )

def get_static_venue_data(venue_slug: str):
    url = build_static_venue_url(venue_slug)
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        handle_http_error(response)
    except RequestException as req_err:
        raise VenueDataServiceError(message=f"Error connecting to the Home Assignment API: {req_err}")

def get_dynamic_venue_data(venue_slug: str):
    url = build_dynamic_venue_url(venue_slug)
    print(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        handle_http_error(response)
    except RequestException as req_err:
        raise VenueDataServiceError(message=f"Error connecting to the Home Assignment API: {req_err}")
    
def parse_venue_data(static_venue_data, dynamic_venue_data) -> VenueData :
    try:
        venue_coordinates = static_venue_data['venue_raw']['location']['coordinates']
        coordinates = Coordinates(latitude=venue_coordinates[1],longitude=venue_coordinates[0])
        min_cart_value = dynamic_venue_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
        base_price = dynamic_venue_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
        distance_ranges = dynamic_venue_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']
        venue_data = {
            "venue_coordinates": coordinates,
            "min_cart_value": min_cart_value,
            "base_price": base_price,
            "distance_ranges": distance_ranges
        }
        return venue_data
    except KeyError as error:
        raise ValueError(f"Missing required key in input data: {error}")

def get_venue_data(venue_slug: str) -> VenueData :
    static_venue_data = get_static_venue_data(venue_slug)
    dynamic_venue_data = get_dynamic_venue_data(venue_slug)
    return parse_venue_data(static_venue_data, dynamic_venue_data)