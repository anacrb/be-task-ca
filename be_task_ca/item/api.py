from fastapi import APIRouter, Depends, HTTPException

from .exceptions import ItemAlreadyExist
from .persistence.in_memory import InMemoryItemRepository, get_in_memory_item_repository
from .usecases import ManageItem

from .schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
        item: CreateItemRequest,
        # db_interface: ItemRepositorySQLAlchemy = Depends(get_item_repository) # This is replaced by the in memory implementation
        db_interface: InMemoryItemRepository = Depends(get_in_memory_item_repository)
) -> CreateItemResponse:
    try:
        manage_item = ManageItem(db_interface)
        return manage_item.create_item(item)
    except ItemAlreadyExist as e:
        raise HTTPException(
            status_code=409, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )


@item_router.get("/")
async def get_items(
        # db_interface: ItemRepositorySQLAlchemy = Depends(get_item_repository) # This is replaced by the in memory implementation
        db_interface: InMemoryItemRepository = Depends(get_in_memory_item_repository)
):
    try:
        manage_item = ManageItem(db_interface)
        return manage_item.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )
