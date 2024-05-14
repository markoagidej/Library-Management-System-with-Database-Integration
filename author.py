
class Author:
    def __init__(self, name, biography):
        self.__name = name
        self.__biography = biography

    def get_name(self):
        return self.__name

    def get_biography(self):
        return self.__biography

    def __str__(self):
        return self.__name
    
def author_collection_add(name, bio, collection):    
    new_author = Author(name, bio)
    if collection:
        collection.append(new_author)
    else:
        collection = [new_author]
    return collection