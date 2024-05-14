
class User:
    def __init__(self, name, UUID, borrow_history = []):
        self.__name = name
        self.__UUID = UUID
        self.__borrow_history = borrow_history

    def get_name(self):
        return self.__name

    def get_UUID(self):
        return self.__UUID

    def get_borrow_history(self):
        return self.__borrow_history

    def add_to_borrow_history(self, book):
        self.__borrow_history.append(book.get_title())
        return self
    
def user_collection_add(name, UUID, collection, borrow_history = []):
    new_user = User(name, UUID, borrow_history)
    if collection:
        collection[UUID] = new_user
    else:
        collection = {UUID: new_user}
    return collection

def notify_user(user):
    # potentially send email or something
    pass