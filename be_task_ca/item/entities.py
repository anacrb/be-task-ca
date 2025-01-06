from uuid import UUID, uuid4

from pydantic.main import BaseModel


class Item(BaseModel):

    id: UUID = uuid4()
    name: str
    description: str
    price: float
    quantity: int