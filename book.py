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
        query = "SELECT availability FROM books WHERE isbn = %s AND available = 1"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue searching for book availability by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            if result:
                return result[0]
            else:
                return False

def get_available_book_id(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT id FROM books WHERE isbn = %s AND available = 1"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue searching for book.id by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return result[0]

def borrow_book(given_user_id = "", given_book_id = ""):
    # Need to check if user exists
    if given_user_id:
        user_id = given_user_id
    else:
        user_id = input("Enter the library id of who would like to borrow a book: ")
        user_check = user_mod.check_user_exists(user_id)
        if not user_check:
            if user_check is None:
                return
            print("No user found with that library id!")
            return
    if not given_book_id:
        # Need to check if book exists
        ISBN = input("Enter the ISBN of the book to be borrowed: ")
        book_check = check_book_exists(ISBN)
        if not book_check:
            if book_check is None:
                return
            print("No book found with that ISBN!")
            return
    # Opening connection
    conn, cursor = connect_db()
    if conn is not None:
        if given_book_id: # Will get here if book was returned and had resrvation
            # Adding an entry into the 'borrowed_books'
            date_today = datetime.datetime.now()
            date_return = date_today + datetime.timedelta(days=7)
            borrow_details = (user_id, given_book_id, date_today, date_return)
            query_add_borrowed_history = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(query_add_borrowed_history, borrow_details)
                conn.commit()
            except Error as e:
                print("Issue adding returned book to borrowed books with reserved user:")
                print(f"Error: {e}")
        else: # if not given_book_id
            # Checking if book is already borrowed
            check_available = check_book_available(ISBN)
            if check_available:
                # Getting book.id of relevant available book
                book_id = get_available_book_id(ISBN)
                # Updating the availability status in 'books'
                book_id_value = (book_id,)
                query_toggle_available = "UPDATE books SET availability 0 WHERE id = %s"
                try:
                    cursor.execute(query_toggle_available, book_id_value)
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
                # If check_available connection failed, should reach here 
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
    user_id = input("Enter the library_id of the person who wants to return a book: ")
    # Checking user exists
    user_check = user_mod.check_user_exists(user_id)
    if not user_check:
        if user_check is None:
            return
        print("No user found with that library id!")
        return
    # Getting list of book ids that user currently has borrowed
    borrowed_books = user_mod.get_user_borrowed_books(user_id)
    # Check if there are any books at all in the list
    if not borrowed_books:
        print(f"User {user_id} has no borrowed books!")
        return
    # Display all books then ask input for which one to return
    conn, cursor = connect_db()
    if conn is not None:
        book_counter = 0
        book_id_list = ["index filler"] # Purpose of index filler is to directly take later input for selected book without performing math
        for book_id in borrowed_books:
            book_counter += 1
            query_get_book_detail = f"SELECT * FROM books WHERE book_id = {book_id[0]}"
            cursor.execute(query_get_book_detail)
            book_details = cursor.fetchone()
            print(f"{book_counter}. {book_details[1]}")
            book_id_list.append(book_details[0])
        if book_counter > 1:
            while True:
                choice = input(f"Which number book is being returned? (1-{book_counter}): ")
                if choice < 1 or choice > book_counter:
                    print(f"Only select a number between 1 and {book_counter}!")
                    continue
                break
        else:
            print(f"This is the only book currently borrowed by {user_id}.")
            cont_choice = input("Do you want to return this book? (y/n): ")
            if cont_choice == "y":
                choice = 1
            else:
                print("No books returned!")
                return
        # Removing book from borrowed books
        try:
            cursor.execute("SET SQL_SAFE_UPDATES = 0")
            query_remove_from_borrowed = f"DELETE FROM borrowed_books WHERE book_id = {book_id_list[choice]}"
            cursor.execute(query_remove_from_borrowed)
            cursor.execute("SET SQL_SAFE_UPDATES = 1")
            print("Book returned!")
        except Error as e:
            print("Issue removing entry from borrowed books!")
            print(f"Error: {e}")
            close_connection()
            return
        # Selecting next user to lend to from reserve list
        try:
            query_check_if_reserved = f"SELECT user_id FROM book_reservations WHERE book_id = {book_id_list[choice]} ORDER BY id ASC"
            cursor.execute(query_check_if_reserved)
            next_user = cursor.fetchone()
            if next_user:
                next_user_id = next_user[0]
            else:
                next_user_id = None
        except Error as e:
            print("Issue getting next reserved user!")
            print(f"Error: {e}")
            close_connection()
            return
        # Toggling availablility in books (if there is a next user found in reservervations, no need to alter availability but need to reborrow the book to next user)
        if next_user_id is None:
            query_set_availability = f"UPDATE books SET availability = 1 WHERE id = {book_id_list[choice]}"
            cursor.execute(query_set_availability)
        else:
            borrow_book(next_user_id, book_id_list[choice])

def get_reservations():
    pass