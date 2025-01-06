import hashlib
from uuid import UUID

from .entities import User, CartItem
from .exceptions import UserAlreadyExist, UserDoesNotExist, ItemDoesNotExist, NotEnoughItemsInStock, ItemAlreadyInCart
from .interfaces import UserDBRepositoryInterface, UserItemDBRepositoryInterface
from ..item.entities import Item



from .schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)

class ManageUser:
    # This class could be divided into two classes to prevent error if the item_db is not provided.
    def __init__(self, user_db: UserDBRepositoryInterface, item_db: UserItemDBRepositoryInterface = None):
        self.user_db = user_db
        self.item_db = item_db


    def create_user(self, create_user: CreateUserRequest) -> CreateUserResponse:
        search_result = self.user_db.find_user_by_email(create_user.email)
        if search_result is not None:
            raise UserAlreadyExist
        new_user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            hashed_password=hashlib.sha512(
                create_user.password.encode("UTF-8")
            ).hexdigest(),
            shipping_address=create_user.shipping_address,
        )

        new_user = self.user_db.save_user(new_user)

        return CreateUserResponse(**new_user.dict())


    def add_item_to_cart(self, user_id: UUID, cart_item: AddToCartRequest) -> AddToCartResponse:
        user = self.user_db.find_user_by_id(user_id)
        if user is None:
            raise UserDoesNotExist

        item: Item = self.item_db.find_item_by_id(cart_item.item_id)
        if item is None:
            raise ItemDoesNotExist
        if item.quantity < cart_item.quantity:
            raise NotEnoughItemsInStock

        item_ids = [o.item_id for o in user.cart_items]
        if cart_item.item_id in item_ids:
            raise ItemAlreadyInCart

        new_cart_item = CartItem(
            user_id=user.id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity
        )

        user.cart_items.append(new_cart_item)

        self.user_db.save_user(user)

        return self.list_items_in_cart(user.id)


    def list_items_in_cart(self, user_id: UUID) -> AddToCartResponse:
        cart_items = self.user_db.find_cart_items_for_user_id(user_id)
        return AddToCartResponse(items=list(map(cart_item_model_to_schema, cart_items)))


def cart_item_model_to_schema(model: CartItem):
    return AddToCartRequest(item_id=model.item_id, quantity=model.quantity)
