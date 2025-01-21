from app.utils import calculate_distance

def test_calculate_distance():
    # Khoảng cách giữa hai điểm gần Helsinki
    lat1, lon1 = 60.17094, 24.93087
    lat2, lon2 = 60.17080, 24.93080
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    assert round(distance) == 16
