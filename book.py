import user as user_mod
import author as author_mod
import genre as genre_mod
from database_connector import connect_db, close_connection
from mysql.connector import Error
import datetime

# class Book:
#     def __init__(self, title, author_id, genre, ISBN, publication_date, available = True):
#         self.__title = title
#         self.__author_id = author_id
#         self.__genre = genre
#         self.__ISBN = ISBN
#         self.__publication_date = publication_date
#         self.__available = available

#     def get_title(self):
#         return self.__title

#     def get_author_id(self):
#         return self.__author_id

#     def get_genre(self):
#         return self.__genre

#     def get_ISBN(self):
#         return self.__ISBN

#     def get_publication_date(self):
#         return self.__publication_date

#     def get_available(self):
#         return self.__available
    
def book_collection_add():
    title = input("Enter the title for the new book: ")

    # Checks if author is already in collection, if not, begins the process to add the author using the input name.
    author = input("Enter the author for the new book: ")
    author_lower = author.lower()
    check_author = author_mod.check_author_exists(author_lower)
    if not check_author:
        # If check connection is bad, break out of function without doing anything
        if check_author is None:
            return
        print("Adding new author to collection!")
        author_mod.author_collection_add(author)
    author_id = author_mod.get_author_id_by_name(author_lower)

    ISBN = input("Enter the ISBN for the new book: ")

    # Checks if genre is already in collection, if not, begins the process to add the genre using the input name.
    genre = input("Enter the genre for the new book: ")
    genre_lower = genre.lower()
    check_genre = genre_mod.check_genre_exists(genre_lower)
    if not check_genre:
        # If check connection is bad, break out of function without doing anything
        if check_genre is None:
            return
        print("Adding new genre to collection!")
        genre_mod.genre_collection_add(genre)
    genre_id = genre_mod.get_genre_id_by_name(genre_lower)

    publication_date = input("Enter the publication date for the new book: ")

    # Connecting to db and updating books table
    conn, cursor = connect_db()
    if conn is not None:
        details = (title, author_id, ISBN, genre_id, publication_date)
        query = "INSERT INTO books (title, author_id, isbn, genre_id, publication_date) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, details)
            conn.commit()
            print(f"{title} added to books!")
        except Error as e:
            print("Issue adding book to database:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def check_book_exists(ISBN):
    conn, cursor = connect_db()
    if conn is not None:
        isbn_value = (ISBN,)
        query = "SELECT * FROM books WHERE isbn = %s"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue searching for book by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(result)

def check_book_available(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT availability FROM books WHERE isbn = %s"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue searching for book availability by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return result[0]

def get_book_id(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT id FROM books WHERE isbn = %s"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue searching for book.id by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return result[0]

def borrow_book():
    # Need to check if user exists
    user_id = input("Enter the library id of who would like to borrow a book: ")
    user_check = user_mod.check_user_exists(user_id)
    if not user_check:
        if user_check is None:
            return
        print("No user found with that library id!")
        return
    # Need to check if book exists
    ISBN = input("Enter the ISBN of the book to be borrowed: ")
    book_check = check_book_exists(ISBN)
    if not book_check:
        if book_check is None:
            return
        print("No book found with that ISBN!")
        return
    # Getting book.id of relevant book
    book_id = get_book_id(ISBN)
    # Opening connection
    conn, cursor = connect_db()
    if conn is not None:
        # Checking if book is already borrowed
        check_available = check_book_available(ISBN)
        if check_available:
            # Updating the availability status in 'books'
            isbn_value = (ISBN,)
            query_toggle_available = "UPDATE books SET availability 0 WHERE isbn = %s"
            try:
                cursor.execute(query_toggle_available, isbn_value)
                # conn.commit() # No commit here since we want both of these actions to successfully take place before making changes to the database
            except Error as e:
                print("Issue updating availability of book being borrowed:")
                print(f"Error {e}")

            # Adding an entry into the 'borrowed_books'
            date_today = datetime.datetime.now()
            date_return = date_today + datetime.timedelta(days=7)
            borrow_details = (user_id, book_id, date_today, date_return)
            query_add_borrowed_history = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(query_add_borrowed_history, borrow_details)
                conn.commit()
            except Error as e:
                print("Issue adding entry to borrowed books:")
                print(f"Error: {e}")
        # If book is borrowed, ask to add to reservation list
        else:
            # If check connection failed, should reach here 
            if check_available is None:
                return
            # Requeset to add to reservation list, then adding to list
            choice = input("That book is already borrowed! Would you like to be added to the reservation list? (y/n): ")
            if choice == "y":
                reserved_values = (user_id, book_id)
                query_add_resreved = "INSERT INTO book_reservations (user_id, book_id)"
                try:
                    cursor.execute(query_add_resreved, reserved_values)
                    conn.commit()
                except Error as e:
                    print("Issue adding entry to book reservations:")
                    print(f"Error: {e}")
        close_connection(conn, cursor)

def return_book():
    if self.__available:
        print("This book is not currently borrowed!")
        return self, ""
    else:
        if self.get_resrvations():
            pass
    self.__available = True
    return self

def get_reservations():
    pass