from typing import Optional, List

from be_task_ca.item.entities import Item
from be_task_ca.item.interfaces import ItemDBRepositoryInterface


class InMemoryItemRepository(ItemDBRepositoryInterface):
    def __init__(self):
        self.items = {}  # Dictionary to store items by name as the key

    def find_item_by_name(self, name: str) -> Optional[Item]:
        return self.items.get(name)

    def get_all_items(self) -> List[Item]:
        return list(self.items.values())

    def save_item(self, item: Item) -> Item:
        self.items[item.name] = item
        return item


def get_in_memory_item_repository() -> InMemoryItemRepository:
    return InMemoryItemRepository()