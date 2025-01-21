import requests
from app.utils import calculate_distance

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

def fetch_venue_data(venue_slug: str):
    """
    Fetch static and dynamic data for a given venue.
    """
    static_url = f"{BASE_URL}/{venue_slug}/static"
    dynamic_url = f"{BASE_URL}/{venue_slug}/dynamic"

    static_response = requests.get(static_url)
    dynamic_response = requests.get(dynamic_url)

    if static_response.status_code != 200 or dynamic_response.status_code != 200:
        raise ValueError("Failed to fetch venue data.")

    return static_response.json(), dynamic_response.json()

def calculate_delivery_price(cart_value: int, user_lat: float, user_lon: float, venue_slug: str):
    """
    Calculate the total delivery price and breakdown for an order.
    """
    static_data, dynamic_data = fetch_venue_data(venue_slug)

