class UserAlreadyExist(Exception):
    def __init__(self):
        super().__init__("An item with this name already exists")