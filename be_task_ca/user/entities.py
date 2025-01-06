from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class CartItem(BaseModel):
    user_id: UUID
    item_id: UUID
    quantity: int


class User(BaseModel):
    user_id: UUID = uuid4()
    name: Optional[str]
    id: UUID = uuid4()
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str]
    cart_items: Optional[List[CartItem]]