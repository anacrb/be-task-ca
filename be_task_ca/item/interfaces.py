from abc import ABC, abstractmethod
from typing import Optional, List

from be_task_ca.item.entities import Item


class ItemDBRepositoryInterface(ABC):

    @abstractmethod
    def find_item_by_name(self, name: str) -> Optional[Item]:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        pass

    @abstractmethod
    def save_item(self, item: Item) -> Item:
        pass