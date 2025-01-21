from fastapi import FastAPI

app = FastAPI()

# Dữ liệu mẫu cho venue (nhà hàng/cửa hàng)
venues_data = {
    "home-assignment-venue-helsinki": {
        "location": [24.93087, 60.17094],  # Vị trí của venue (longitude, latitude)
        "order_minimum_no_surcharge": 1000,  # Giá trị đơn hàng tối thiểu để không bị phụ phí nhỏ
        "delivery_specs": {
            "base_price": 150,  # Phí giao hàng cơ bản
            "distance_ranges": [
                {"min": 0, "max": 500, "a": 0, "b": 0},
                {"min": 500, "max": 1000, "a": 100, "b": 1},
                {"min": 1000, "max": 0, "a": 0, "b": 0},  # Không giao hàng nếu khoảng cách > 1000m
            ]
        }
    }
}

# Hàm tính khoảng cách giữa hai điểm (sử dụng công thức Haversine)
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Đổi độ sang radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Công thức Haversine để tính khoảng cách
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Bán kính trái đất (km)
    radius = 6371.0
    distance = radius * c  # Đơn vị tính là km
    return distance * 1000  # Đổi sang mét

@app.get("/")
def read_root():
    return {"message": "Welcome to the Delivery Order Price Calculator!"}

@app.get("/api/v1/delivery-order-price")
def get_delivery_order_price(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    # Kiểm tra xem venue_slug có tồn tại trong dữ liệu không
    venue = venues_data.get(venue_slug)
    if not venue:
        return {"error": "Venue not found"}, 404

    # Lấy thông tin của venue
    venue_location = venue["location"]
    order_minimum_no_surcharge = venue["order_minimum_no_surcharge"]
    delivery_specs = venue["delivery_specs"]

    # Tính phụ phí đơn hàng nhỏ
    small_order_surcharge = max(0, order_minimum_no_surcharge - cart_value)

    # Tính khoảng cách giao hàng
    delivery_distance = calculate_distance(user_lat, user_lon, venue_location[1], venue_location[0])

    # Tính phí giao hàng
    base_price = delivery_specs["base_price"]
    delivery_fee = base_price
    for range in delivery_specs["distance_ranges"]:
        if range["min"] <= delivery_distance < range["max"]:
            delivery_fee += range["a"] + range["b"] * (delivery_distance / 10)

    # Nếu khoảng cách quá xa (lớn hơn 1000m), trả về lỗi
    if delivery_distance > 1000:
        return {"error": "Delivery is not possible for the given distance"}, 400

    # Tính tổng giá
    total_price = cart_value + small_order_surcharge + delivery_fee

    return {
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": int(delivery_distance)  # Làm tròn khoảng cách về số nguyên
        }
    }
