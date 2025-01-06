from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from .exceptions import UserAlreadyExist, UserDoesNotExist, ItemDoesNotExist, NotEnoughItemsInStock, ItemAlreadyInCart
from .persistence.SQLAlquemy import UserRepositorySQLAlchemy, get_user_repository, UserItemRepositorySQLAlchemy, \
    get_user_item_repository
from .persistence.in_memory import InMemoryUserRepository, get_in_memory_user_repository, InMemoryUserItemRepository, \
    get_in_memory_user_item_repository

from .usecases import ManageUser

from .schema import AddToCartRequest, CreateUserRequest


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/")
async def post_customer(
        user: CreateUserRequest,
        # db_interface: UserRepositorySQLAlchemy = Depends(get_user_repository)  # This is replaced by the in memory implementation
        db_interface: InMemoryUserRepository = Depends(get_in_memory_user_repository)
):
    try:
        manage_user = ManageUser(db_interface)
        return manage_user.create_user(user)
    except UserAlreadyExist as e:
        raise HTTPException(
            status_code=409, detail=str(e)
        )


@user_router.post("/{user_id}/cart")
async def post_cart(
        user_id: UUID,
        cart_item: AddToCartRequest,
        # db_user_interface: UserRepositorySQLAlchemy = Depends(get_user_repository),  # This is replaced by the in memory implementation
        # db_item_interface: UserItemRepositorySQLAlchemy = Depends(get_item_repository)  # This is replaced by the in memory implementation
        db_user_interface: InMemoryUserRepository = Depends(get_in_memory_user_repository),
        db_item_interface: InMemoryUserItemRepository = Depends(get_in_memory_user_item_repository)
):
    try:
        manage_user = ManageUser(db_user_interface, db_item_interface)
        return manage_user.add_item_to_cart(user_id, cart_item)
    except (
            UserDoesNotExist,
            ItemDoesNotExist
        ) as e:
        raise HTTPException(
            status_code=404, detail=str(e)
        )
    except (
            NotEnoughItemsInStock,
            ItemAlreadyInCart
    ) as e:
        raise HTTPException(
            status_code=409, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )


@user_router.get("/{user_id}/cart")
async def get_cart(
        user_id: UUID,
        # db_interface: UserRepositorySQLAlchemy = Depends(get_user_repository)  # This is replaced by the in memory implementation
        db_interface: InMemoryUserRepository = Depends(get_in_memory_user_repository)
):
    try:
        manage_user = ManageUser(db_interface)
        return manage_user.list_items_in_cart(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )
