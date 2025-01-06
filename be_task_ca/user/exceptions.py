class UserAlreadyExist(Exception):
    def __init__(self):
        super().__init__("An user with this email address already exists")

class UserDoesNotExist(Exception):
    def __init__(self):
        super().__init__("User does not exist")

class ItemDoesNotExist(Exception):
    def __init__(self):
        super().__init__("Item does not exist")

class NotEnoughItemsInStock(Exception):
    def __init__(self):
        super().__init__("Not enough items in stock")

class ItemAlreadyInCart(Exception):
    def __init__(self):
        super().__init__("Item already in cart")