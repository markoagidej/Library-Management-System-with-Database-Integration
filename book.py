import user as user_mod
import author as author_mod
import genre as genre_mod
from database_connector import connect_db, close_connection
from mysql.connector import Error
import datetime
    
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

# Return boolean if book with isbn exists
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

# Return boolean if book of isbn has an available copy
def check_book_available(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT availability FROM books WHERE isbn = %s AND availability = 1"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
            close_connection(conn, cursor)
            if result:
                return result[0]
            else:
                return False
        except Error as e:
            print("Issue searching for book availability by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

# Returns the id of an available copy of a book with input isbn
def get_available_book_id(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT id FROM books WHERE isbn = %s AND availability = 1"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
            if result:
                return result[0]
        except Error as e:
            print("Issue searching for book.id by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def get_next_reserved_book_id(ISBN):
    conn, cursor = connect_db()
    if conn is not None:        
        isbn_value = (ISBN,)
        query = "SELECT borrowed.book_id, b.isbn FROM borrowed_books borrowed, books b WHERE borrowed.book_id = b.id AND b.isbn = %s ORDER BY borrowed.id ASC"
        try:
            cursor.execute(query, isbn_value)
            result = cursor.fetchone()
            if result:
                return result[0]
        except Error as e:
            print("Issue searching for book.id by isbn:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def borrow_book(given_user_id = "", given_book_id = ""):
    # Need to check if user exists
    if given_user_id:
        user_id = given_user_id
    else:
        library_id = input("Enter the library_id of who would like to borrow a book: ")
        user_check = user_mod.check_user_exists_by_library_id(library_id)
        if not user_check:
            if user_check is None:
                return
            print("No user found with that library id!")
            return
        else:
            user_id = user_mod.get_id_by_library_id(library_id)
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
        if given_book_id: # Will get here if book was returned and had reservation
            # Adding an entry into the 'borrowed_books'
            date_today = datetime.datetime.now()
            date_return = date_today + datetime.timedelta(days=7)
            borrow_details = (user_id, given_book_id, date_today, date_return)
            query_add_borrowed_history = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(query_add_borrowed_history, borrow_details)
                print(f"Book automatically lent out to next on reserve list!")
                print(f"Book due on {date_return}")
                conn.commit()
            except Error as e:
                print("Issue adding returned book to borrowed books with reserved user:")
                print(f"Error: {e}")
            remove_details = (user_id, given_book_id)
            query_remove_reservation = "DELETE FROM book_reservations WHERE user_id = %s AND book_id = %s"
            try:                
                cursor.execute("SET SQL_SAFE_UPDATES = 0")
                cursor.execute(query_remove_reservation, remove_details)
                cursor.execute("SET SQL_SAFE_UPDATES = 1")
                conn.commit()
            except Error as e:
                print("Issue removing book resrevation:")
                print(f"Error: {e}")                
        else: # if not given_book_id
            # Checking if book is already borrowed
            check_available = check_book_available(ISBN)
            if check_available:
                # Getting book.id of relevant available book
                book_id = get_available_book_id(ISBN)
                # Updating the availability status in 'books'
                book_id_value = (book_id,)
                query_toggle_available = "UPDATE books SET availability = 0 WHERE id = %s"
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
                    print(f"Book due on {date_return}")
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
                    book_id = get_next_reserved_book_id(ISBN)
                    reserved_values = (user_id, book_id)
                    query_add_resreved = "INSERT INTO book_reservations (user_id, book_id) VALUES (%s, %s)"
                    try:
                        cursor.execute(query_add_resreved, reserved_values)
                        conn.commit()
                        print(f"Book reserved for library_id {library_id}!")
                    except Error as e:
                        print("Issue adding entry to book reservations:")
                        print(f"Error: {e}")
        close_connection(conn, cursor)

def return_book():
    library_id = input("Enter the library_id of the person who wants to return a book: ")
    # Checking user exists
    user_check = user_mod.check_user_exists_by_library_id(library_id)
    if not user_check:
        if user_check is None:
            return
        print("No user found with that library id!")
        return
    # Getting list of book ids that user currently has borrowed
    borrowed_books = user_mod.get_user_borrowed_books_by_library_id(library_id)
    # Check if there are any books at all in the list
    if not borrowed_books:
        print(f"User {library_id} has no borrowed books!")
        return
    # Display all books borrowed by user then ask input for which one to return
    conn, cursor = connect_db()
    if conn is not None:
        book_counter = 0
        book_id_list = ["index filler"] # Purpose of index filler is to directly take later input for selected book without performing math
        for book in borrowed_books:
            book_counter += 1
            book_id_value = (book[2],)
            query_get_book_detail = "SELECT * FROM books WHERE id = %s"
            try:
                cursor.execute(query_get_book_detail, book_id_value)
                book_details = cursor.fetchone()
                print(f"{book_counter}. {book_details[1]}")
                book_id_list.append(book_details[0])
            except Error as e:
                print("Problem dispalying borrowed book for user!")
                print(f"Error {e}")
        if book_counter > 1:
            while True:
                choice = input(f"Which number book is being returned? (1-{book_counter}): ")
                if choice < 1 or choice > book_counter:
                    print(f"Only select a number between 1 and {book_counter}!")
                    continue
                break
        else:
            print(f"This is the only book currently borrowed by {library_id}.")
            cont_choice = input("Do you want to return this book? (y/n): ")
            if cont_choice == "y":
                choice = 1
            else:
                print("No books returned!")
                return
        # Removing book from borrowed books
        book_id_choice_value = (book_id_list[choice],)
        try:
            cursor.execute("SET SQL_SAFE_UPDATES = 0")
            query_remove_from_borrowed = "DELETE FROM borrowed_books WHERE book_id = %s"
            cursor.execute(query_remove_from_borrowed, book_id_choice_value)
            cursor.execute("SET SQL_SAFE_UPDATES = 1")
            conn.commit()
            print("Book returned!")
        except Error as e:
            print("Issue removing entry from borrowed books!")
            print(f"Error: {e}")
            close_connection()
            return
        # Selecting next user to lend to from reserve list
        try:
            query_check_if_reserved = "SELECT user_id FROM book_reservations WHERE book_id = %s ORDER BY id ASC"
            cursor.execute(query_check_if_reserved, book_id_choice_value)
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
            query_set_availability = "UPDATE books SET availability = 1 WHERE id = %s"
            cursor.execute(query_set_availability, book_id_choice_value)
        else:
            borrow_book(next_user_id, book_id_list[choice])
        conn.commit()
        close_connection(conn, cursor)

def search_book():
    search = input("Enter part of the title of the book you would like to search: ")
    search_lower_pattern = f"%{search.lower()}%"
    conn, cursor = connect_db()
    if conn is not None:
        search_value = (search_lower_pattern,)
        query_search = "SELECT * FROM books WHERE LOWER(title) LIKE %s"
        try:
            cursor.execute(query_search, search_value)
            book_list = cursor.fetchall()
        except Error as e:
            print("Issue searching for books:")
            print(f"Error: {e}")
            close_connection(conn, cursor)
            return
        if book_list:
            print(f"Here are all the books with \'{search}\' in the title:")
            for book in book_list:
                print(f"- {book[1]}")
        else:
            print(f"No books found with {search} in the title!")

def display_all_books():
    conn, cursor = connect_db()
    if conn is not None:
        query = "SELECT * FROM books"
        try:
            cursor.execute(query)
            print("id|title|author|genre|isbn|publication_date|available")
            book_list = cursor.fetchall()
            for book in book_list:
                author = author_mod.get_author_name_by_id(book[2])
                genre = genre_mod.get_genre_name_by_id(book[3])
                print(f"{book[0]}|{book[1]}|{author}|{genre}|{book[4]}|{book[5]}|{book[6]}")
        except Error as e:
            print("Problem dispalying all books!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)