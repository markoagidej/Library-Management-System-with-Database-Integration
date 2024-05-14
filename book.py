import user as user_mod

class Book:
    def __init__(self, title, author, ISBN, genre, publication_date, available = True, reserve_list = []):
        self.__title = title
        self.__author = author
        self.__ISBN = ISBN
        self.__genre = genre
        self.__publication_date = publication_date
        self.__available = available
        self.__reserve_list = reserve_list

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_ISBN(self):
        return self.__ISBN

    def get_genre(self):
        return self.__genre

    def get_publication_date(self):
        return self.__publication_date

    def get_available(self):
        return self.__available

    def get_reserve_list(self):
        return self.__reserve_list
    
    def borrow_book(self, user_ID):
        if self.__available:
            self.__available = False
        else:
            choice = input("Would you like to be put on the reserve list for this book? (y/n): ")
            if choice == "y":
                self.__reserve_list.append(user_ID)
                print(f"{user_ID} added to the reservation list for {self.__title}")
        return self

    def return_book(self):
        if self.__available:
            print("This book is not currently borrowed!")
            return self, ""
        else:
            if self.__reserve_list:
                next_reserved_user_ID = self.__reserve_list.pop(0)
            else:
                next_reserved_user_ID = ""
        self.__available = True
        return self, next_reserved_user_ID

class Book_Fiction(Book):
    def __init__(self, title, author, ISBN, genre, publication_date, available = True, reserve_list = []):
        super().__init__(title, author, ISBN, genre, publication_date, available, reserve_list)

    def __str__(self):
        print("A work of fiction")

class Book_Non_Fiction(Book):
    def __init__(self, title, author, ISBN, genre, publication_date, available = True, reserve_list = []):
        super().__init__(title, author, ISBN, genre, publication_date, available, reserve_list)

    def __str__(self):
        print("A work of truth")

class Book_Mystery(Book):
    def __init__(self, title, author, ISBN, genre, publication_date, available = True, reserve_list = []):
        super().__init__(title, author, ISBN, genre, publication_date, available, reserve_list)

    def __str__(self):
        print("Who knows?")        

def book_collection_add(title, author, ISBN, genre, publication_date, collection = {}, available = True, res_list = [], type = 4):
    if type == 1:
        new_book = Book_Fiction(title, author, ISBN, genre, publication_date, available, res_list)
    elif type == 2:
        new_book = Book_Non_Fiction(title, author, ISBN, genre, publication_date, available, res_list)
    elif type == 3:
        new_book = Book_Mystery(title, author, ISBN, genre, publication_date, available, res_list)
    else:
        new_book = Book(title, author, ISBN, genre, publication_date, available, res_list)
        
    if collection:
        collection[ISBN] = new_book
    else:
        collection = {ISBN: new_book}
    return collection