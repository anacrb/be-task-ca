from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, List

from be_task_ca.common import get_db
from be_task_ca.item.entities import Item
from be_task_ca.item.persistence.model import ItemModel
from be_task_ca.user.entities import User, CartItem
from be_task_ca.user.interfaces import UserDBRepositoryInterface, UserItemDBRepositoryInterface
from be_task_ca.user.persistence.model import UserModel, CartItemModel


class UserRepositorySQLAlchemy(UserDBRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_user_by_email(self, email: str) -> Optional[User]:
        user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
        if user:
            return User(**user.to_dict())
        return None

    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            return User(**user.to_dict())
        return None

    def save_user(self, user: User) -> User:
        new_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        return User(**new_user.to_dict())

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        cart_items = self.db_session.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()
        return [CartItem(**ci.to_dict()) for ci in cart_items]


def get_user_repository(db_session: Session = Depends(get_db)) -> UserRepositorySQLAlchemy:
    return UserRepositorySQLAlchemy(db_session)


class UserItemRepositorySQLAlchemy(UserItemDBRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_item_by_id(self, id: UUID) -> Item:
        item = self.db_session.query(ItemModel).filter(ItemModel.id == id).first()
        return Item(**item.to_dict())


def get_user_item_repository(db_session: Session = Depends(get_db)) -> UserItemRepositorySQLAlchemy:
    return UserItemRepositorySQLAlchemy(db_session)