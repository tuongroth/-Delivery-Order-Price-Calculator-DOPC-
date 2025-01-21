import requests
import math

# Hàm tính khoảng cách giữa hai điểm theo vĩ độ và kinh độ
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Bán kính trái đất tính theo km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c  # khoảng cách theo km
    distance_m = distance_km * 1000  # chuyển sang mét
    return distance_m

# Hàm lấy thông tin từ Home Assignment API
def get_venue_data(venue_slug):
    static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
    dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"

    static_data = requests.get(static_url).json()
    dynamic_data = requests.get(dynamic_url).json()

    venue_location = static_data["venue_raw"]["location"]["coordinates"]
    order_minimum_no_surcharge = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
    base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
    distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]

    return venue_location, order_minimum_no_surcharge, base_price, distance_ranges

# Hàm tính phí giao hàng
def calculate_delivery_fee(distance, base_price, distance_ranges):
    for range in distance_ranges:
        if range["min"] <= distance < range["max"] or range["max"] == 0:
            fee = base_price + range["a"] + round(range["b"] * distance / 10)
            return fee
    return None  # Trường hợp nếu khoảng cách quá xa (không có phạm vi hợp lệ)

# Hàm tính giá trị đơn hàng
def calculate_order_price(venue_slug, cart_value, user_lat, user_lon):
    # Lấy dữ liệu từ Home Assignment API
    venue_location, order_minimum_no_surcharge, base_price, distance_ranges = get_venue_data(venue_slug)

    # Tính khoảng cách giữa người dùng và địa điểm
    venue_lat, venue_lon = venue_location
    distance = calculate_distance(user_lat, user_lon, venue_lat, venue_lon)

    # Tính phụ thu đơn hàng nhỏ
    small_order_surcharge = max(0, order_minimum_no_surcharge - cart_value)

    # Tính phí giao hàng
    delivery_fee = calculate_delivery_fee(distance, base_price, distance_ranges)

    if delivery_fee is None:
        raise ValueError("Delivery is not possible due to distance being too far.")

    # Tính tổng giá trị đơn hàng
    total_price = cart_value + small_order_surcharge + delivery_fee

    # Tạo JSON kết quả
    return {
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": round(distance)
        }
    }

# Hàm chạy API
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/v1/delivery-order-price", methods=["GET"])
def delivery_order_price():
    try:
        venue_slug = request.args.get("venue_slug")
        cart_value = int(request.args.get("cart_value"))
        user_lat = float(request.args.get("user_lat"))
        user_lon = float(request.args.get("user_lon"))

        result = calculate_order_price(venue_slug, cart_value, user_lat, user_lon)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
