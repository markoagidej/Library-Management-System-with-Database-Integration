import user as user_mod

class Book:
    def __init__(self, title, author_id, genre, ISBN, publication_date, available = True):
        self.__title = title
        self.__author_id = author_id
        self.__genre = genre
        self.__ISBN = ISBN
        self.__publication_date = publication_date
        self.__available = available

    def get_title(self):
        return self.__title

    def get_author_id(self):
        return self.__author_id

    def get_genre(self):
        return self.__genre

    def get_ISBN(self):
        return self.__ISBN

    def get_publication_date(self):
        return self.__publication_date

    def get_available(self):
        return self.__available
    
    def borrow_book(self, user_ID):
        if self.__available:
            self.__available = False
        else:
            choice = input("Would you like to be put on the reserve list for this book? (y/n): ")
            if choice == "y":
                pass
                print(f"{user_ID} added to the reservation list for {self.__title}")
        return self

    def return_book(self):
        if self.__available:
            print("This book is not currently borrowed!")
            return self, ""
        else:
            if self.get_resrvations():
                pass
        self.__available = True
        return self
    
    def get_resrvations(self):
        pass      

def book_collection_add(title, author_id, genre, ISBN, publication_date, collection = {}, available = True):
    new_book = Book(title, author_id, genre, ISBN, publication_date, available)
        
    if collection:
        collection[ISBN] = new_book
    else:
        collection = {ISBN: new_book}
    return collection