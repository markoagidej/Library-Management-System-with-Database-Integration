
class Genre:
    def __init__(self, name, description, category):
        self.__name = name
        self.__description = description
        self.__category = category

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_category(self):
        return self.__category
    
    def __str__(self):
        return self.__name
    
def genre_collection_add(name, description, category, collection):    
    new_genre = Genre(name, description, category)
    if collection:
        if new_genre in collection:
            print(f"Genre \'{name}\' in category \'{category}\' already exists!")
            return collection
        collection.append(new_genre)
    else:
        collection = [new_genre]
    return collection