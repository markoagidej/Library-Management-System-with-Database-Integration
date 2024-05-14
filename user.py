
class User:
    def __init__(self, name, library_uuid):
        self.__name = name
        self.__library_uuid = library_uuid

    def get_name(self):
        return self.__name

    def get_library_uuid(self):
        return self.__library_uuid
    
def user_collection_add(name, library_uuid, collection):
    new_user = User(name, library_uuid)
    if collection:
        collection[library_uuid] = new_user
    else:
        collection = {library_uuid: new_user}
    return collection

def notify_user(user):
    # potentially send email or something
    pass