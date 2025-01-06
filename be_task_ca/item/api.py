from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .exceptions import UserAlreadyExist
from .persistence.SQLAlquemy import ItemRepositorySQLAlchemy, get_item_repository
from .usecases import create_item, get_all, ManageItem

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
        item: CreateItemRequest,
        db_interface: ItemRepositorySQLAlchemy = Depends(get_item_repository)
) -> CreateItemResponse:
    try:
        manage_item = ManageItem(db_interface)
        return manage_item.create_item(item)
    except UserAlreadyExist as e:
        raise HTTPException(
            status_code=409, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )


@item_router.get("/")
async def get_items(db_interface: ItemRepositorySQLAlchemy = Depends(get_item_repository)):
    try:
        manage_item = ManageItem(db_interface)
        return manage_item.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )
