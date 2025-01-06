import logging
from typing import Optional, List
from uuid import UUID
from collections import defaultdict

from be_task_ca.item.entities import Item
from be_task_ca.user.entities import User, CartItem
from be_task_ca.user.exceptions import ItemDoesNotExist
from be_task_ca.user.interfaces import UserDBRepositoryInterface, UserItemDBRepositoryInterface


class InMemoryUserRepository(UserDBRepositoryInterface):
    def __init__(self):
        self.users = {}  # Dictionary to store users by ID
        self.cart_items = defaultdict(list)  # Dictionary to store cart items by user ID

    def find_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.users.get(user_id)

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        return self.cart_items.get(user_id, [])

    def save_user(self, user: User) -> User:
        self.users[user.user_id] = user
        return user

def get_in_memory_user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()

class InMemoryUserItemRepository(UserItemDBRepositoryInterface):
    def __init__(self):
        self.items = {}  # Dictionary to store items by ID

    def find_item_by_id(self, id: UUID) -> Optional[Item]:
        item = self.items.get(id)
        if item:
            return item
        return None

def get_in_memory_user_item_repository() -> InMemoryUserItemRepository:
    return InMemoryUserItemRepository()
