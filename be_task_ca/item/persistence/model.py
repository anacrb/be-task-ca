from dataclasses import dataclass
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from be_task_ca.database import Base


@dataclass
class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4(),
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]

    def to_dict(self):
        """
        Convert the UserModel instance into a dictionary representation.
        Handles relationships by including a simplified list of related items.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
        }
