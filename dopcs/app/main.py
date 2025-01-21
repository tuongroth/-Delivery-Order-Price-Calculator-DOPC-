import math
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

def get_venue_data(venue_slug: str):
    """ Fetches static and dynamic venue data from the Home Assignment API. """
    static_url = f"{BASE_URL}/{venue_slug}/static"
    dynamic_url = f"{BASE_URL}/{venue_slug}/dynamic"
    
    static_response = requests.get(static_url)
    dynamic_response = requests.get(dynamic_url)

    if static_response.status_code != 200 or dynamic_response.status_code != 200:
        return None, None

    static_data = static_response.json()
    dynamic_data = dynamic_response.json()
    
    return static_data, dynamic_data


def calculate_distance(lat1, lon1, lat2, lon2):
    """ Calculate the straight-line distance between two points (in meters). """
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c * 1000  # Convert to meters
    return distance


def calculate_delivery_fee(base_price, distance, distance_ranges):
    """ Calculate the delivery fee based on distance and pricing rules. """
    fee = base_price
    
    for range in distance_ranges:
        if range["min"] <= distance < (range["max"] if range["max"] != 0 else float('inf')):
            fee += range["a"]
            fee += math.round(range["b"] * distance / 10)
            break
    
    return fee


@app.route('/api/v1/delivery-order-price', methods=['GET'])
def get_delivery_price():
    venue_slug = request.args.get('venue_slug')
    cart_value = int(request.args.get('cart_value'))
    user_lat = float(request.args.get('user_lat'))
    user_lon = float(request.args.get('user_lon'))

    static_data, dynamic_data = get_venue_data(venue_slug)
    
    if not static_data or not dynamic_data:
        return jsonify({"error": "Failed to retrieve venue data"}), 400

    venue_lat, venue_lon = static_data['venue_raw']['location']['coordinates']
    order_minimum_no_surcharge = dynamic_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
    base_price = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
    distance_ranges = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']
    
    # Calculate small order surcharge
    small_order_surcharge = max(0, order_minimum_no_surcharge - cart_value)

    # Calculate distance
    distance = calculate_distance(user_lat, user_lon, venue_lat, venue_lon)
    
    # Check if the delivery is possible
    if distance >= distance_ranges[-1]["min"]:
        return jsonify({"error": "Delivery is not possible due to distance being too far."}), 400
    
    # Calculate delivery fee
    delivery_fee = calculate_delivery_fee(base_price, distance, distance_ranges)
    
    # Calculate total price
    total_price = cart_value + small_order_surcharge + delivery_fee
    
    return jsonify({
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": int(distance)
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
