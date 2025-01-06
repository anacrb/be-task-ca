from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from be_task_ca.item.entities import Item
from be_task_ca.user.entities import User, CartItem


class UserDBRepositoryInterface(ABC):

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> User:
        pass


class UserItemDBRepositoryInterface(ABC):

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> Item:
    # NOTE: This interface currently interacts directly with Item for simplicity.
    # In the future, this interaction can be replaced with an inter-service communication mechanism,
    # such as REST, gRPC, or message queues, to decouple User from Item.
    # Ensure that any changes to this interface maintain compatibility with the existing business logic.
        pass