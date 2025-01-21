# dopcs/app/models.py
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class Order(BaseModel):
    item: Item
    quantity: int
