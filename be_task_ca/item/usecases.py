from .entities import Item
from .exceptions import ItemAlreadyExist
from .interfaces import ItemDBRepositoryInterface
from .schema import AllItemsResponse, CreateItemRequest, CreateItemResponse


class ManageItem:
    def __init__(self, db: ItemDBRepositoryInterface):
        self.db = db

    def create_item(self, item: CreateItemRequest) -> CreateItemResponse:
        search_result = self.db.find_item_by_name(item.name)
        if search_result is not None:
            raise ItemAlreadyExist

        new_item = Item(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )

        new_item = self.db.save_item(new_item)
        return model_to_schema(new_item)


    def get_all(self) -> AllItemsResponse:
        item_list = self.db.get_all_items()
        return AllItemsResponse(items=list(map(model_to_schema, item_list)))



def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
