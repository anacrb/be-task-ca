from typing import Optional, List

from fastapi import Depends
from sqlalchemy.orm import Session

from be_task_ca.common import get_db
from be_task_ca.item.entities import Item
from be_task_ca.item.interfaces import ItemDBRepositoryInterface
from be_task_ca.item.persistence.model import ItemModel


class ItemRepositorySQLAlchemy(ItemDBRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_item_by_name(self, name: str) -> Optional[Item]:
        item = self.db_session.query(ItemModel).filter(ItemModel.name == name).first()
        if item:
            return Item(**item.to_dict())
        return None

    def get_all_items(self) -> List[Item]:
        all_items = self.db_session.query(ItemModel).all()
        return [Item(**item.to_dict()) for item in all_items]

    def save_item(self, item: Item) -> Item:
        new_item = ItemModel(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.db_session.add(new_item)
        self.db_session.commit()
        return Item(**new_item.to_dict())

def get_item_repository(db_session: Session = Depends(get_db)) -> ItemRepositorySQLAlchemy:
    return ItemRepositorySQLAlchemy(db_session)