from fastapi import APIRouter, Query, HTTPException
from app.services import calculate_order_price

router = APIRouter()

@router.get("/api/v1/delivery-order-price")
async def delivery_order_price(
    venue_slug: str = Query(..., description="Slug của địa điểm"),
    cart_value: int = Query(..., ge=0, description="Giá trị giỏ hàng"),
    user_lat: float = Query(..., description="Vĩ độ người dùng"),
    user_lon: float = Query(..., description="Kinh độ người dùng")
):
    try:
        response = await calculate_order_price(venue_slug, cart_value, user_lat, user_lon)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
