
import os
import re
import book as book_mod
import user as user_mod
import author as author_mod
import genre as genre_mod
from database_connector import connect_db, close_connection

# book_collection = {} # {ISBN : Book}
# user_collection = {} # {UUID : User}
# author_collection = [] # [Author]
# genre_collection = [] # [Genre]
# text_deliniator = "|"

def populate_collection(table_name):
    global book_collection
    global user_collection
    global author_collection
    global genre_collection
    
    select_query = f"SELECT * from {table_name}"
    conn, cursor = connect_db()
    if conn is not None:
        cursor.execute(select_query)
        results = cursor.fetchall()
        if table_name == "books": # Adds a book object into the book_collection for every entry in the database
            if results:
                for result in results:
                    title = result[1]
                    author_id = result[2]
                    genre_id = result[3]
                    ISBN = result[4]
                    publication_date = result[5]
                    available = result[6]
                    book_collection = book_mod.book_collection_add(title, author_id, genre_id, ISBN, publication_date, book_collection, available)
            else:
                book_collection = {}
        elif table_name == "users": # Adds a user object into the user_collection for every entry in the database
            if results:
                for result in results:
                    name = result[1]
                    library_uuid = result[2]
                    user_collection = user_mod.user_collection_add(name, library_uuid, user_collection)
            else:
                user_collection = {}
        elif table_name == "authors": # Adds an author object into the author_collection for every entry in the database
            if results:
                for result in results:
                    name = result[1]
                    bio = result[2]
                    author_collection = author_mod.author_collection_add(name, bio, author_collection)
            else:
                author_collection = []
        elif table_name == "genres": # Adds a genre object into the genre_collection for every entry in the database
            if results:
                for result in results:
                    name = result[1]
                    description = result[2]
                    category = result[3]
                    genre_collection = genre_mod.genre_collection_add(name, description, category, genre_collection)
            else:
                genre_collection = []
        close_connection(conn, cursor)

def load_file(filename):
    if os.path.exists(f"Files\\{filename}"):
        try:
            with open(f"Files\\{filename}", "r") as file:
                if filename == "books.txt":
                    book_dict = {}
                    for line in file:
                        if not line:
                            break
                        title, author, ISBN, genre, publication_date, available, res_list = line.split(text_deliniator)
                        available_parsed = available != "False"
                        match = re.search("\\[(.*)\\]", res_list)
                        if match.group(1):
                            res_list_parsed = match.group(1).split(",")
                        else:
                            res_list_parsed = []
                        book_dict = book_mod.book_collection_add(title, author, ISBN, genre, publication_date, book_dict, available_parsed, res_list_parsed)
                    return book_dict
                elif filename == "users.txt":
                    user_dict = {}
                    for line in file:
                        if not line:
                            break
                        name, UUID, borrow_list = line.split(text_deliniator)
                        match = re.search("\\[(.*)\\]", borrow_list)                    
                        if match.group(1):
                            borrow_list_parsed = match.group(1).split(",")
                        else:
                            borrow_list_parsed = []
                        user_dict = user_mod.user_collection_add(name, UUID, user_dict, borrow_list_parsed)
                    return user_dict
                elif filename == "authors.txt":
                    authors_list = []
                    for line in file:
                        if not line:
                            break
                        name, bio = line.split(text_deliniator)
                        bio = bio.strip()
                        authors_list = author_mod.author_collection_add(name, bio, authors_list)
                    return authors_list
                elif filename == "genres.txt":
                    genre_list = []
                    for line in file:
                        if not line:
                            break
                        name, description, category = line.split(text_deliniator)
                        genre_list = genre_mod.genre_collection_add(name, description, category, genre_list)
                    return genre_list
        except:
            print(f"File error for \'{filename}\'")
    else: # if no file exists, create one and a default empty data structure
        try:
            with open(f"Files\\{filename}", "w") as file:
                pass
        except:
            print(f"Path issue for \'Files\\{filename}\'")

        if filename == "books.txt":
            return {}
        elif filename == "users.txt":
            return {}
        elif filename == "authors.txt":
            return []
        elif filename == "genres.txt":
            return []

def save_books_file():
    global book_collection
    with open(f"Files\\books.txt", 'w') as file:
        for book in book_collection.values():
            title = book.get_title()
            author = book.get_author()
            ISBN = book.get_ISBN()
            genre = book.get_genre()
            pub_date = book.get_publication_date()
            available = str(book.get_available())
            res_list = "[" + ",".join(book.get_reserve_list()) + "]"
            final_line = "|".join([title, author, ISBN, genre, pub_date, available, res_list])
            file.write(final_line + "\n")
            
def save_users_file():
    global user_collection
    with open(f"Files\\users.txt", "w") as file:
        for user in user_collection.values():
            borrow_test = user.get_borrow_history()
            borrow_list = "[" + ",".join(borrow_test) + "]"
            file.write(text_deliniator.join([user.get_name(), user.get_UUID(), borrow_list]) + "\n")
            
def save_authors_file():
    global author_collection
    with open(f"Files\\authors.txt", "w") as file:
        for author in author_collection:
            file.write(text_deliniator.join([author.get_name(), author.get_biography()]) + "\n")
            
def save_genres_file():
    global genre_collection
    with open(f"Files\\genres.txt", "w") as file:
        for genre in genre_collection:
            file.write(text_deliniator.join([genre.get_name(), genre.get_description(), genre.get_category()]) + "\n")

def main():
    global book_collection
    global user_collection
    global author_collection
    global genre_collection

    populate_collection("books")
    populate_collection("users")
    populate_collection("authors")
    populate_collection("genres")

    while True:
        print("Main Menu:")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")

        try:
            choice = int(input())
        except ValueError:
            print("Only enter a number 1-5")
            continue

        if choice == 1:
            menu_book_ops()
        elif choice == 2:
            menu_user_ops()
        elif choice == 3:
            menu_author_ops()
        elif choice == 4:
            menu_genre_ops()
        elif choice == 5:
            print("Thank you, goodbye!")
            exit()

def menu_book_ops():
    while True:
        print("Book Operations:")
        print("1. Add a new book")
        print("2. Borrow/Reserve a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")

        try:
            choice = int(input())
        except ValueError:
            print("Only enter a number 1-5")
            continue

        if choice == 1: #  Add a new book
            print("Adding a new book to the library!")
            book_mod.book_collection_add()
            break
        elif choice == 2: # Borrow/Reserve a book
            print("Borrowing a book!")
            book_mod.borrow_book()
            break
        elif choice == 3: # Return a book
            print("Returning a book!")
            book_mod.return_book()
            break
        elif choice == 4: # Search for a book
            print("Searching for a book!")
            book_mod.search_book()
            break
        elif choice == 5: # Display all books
            print("Displaying all books in library:")
            book_mod.display_all_books()

def menu_user_ops():
    global user_collection
    while True:
        print("User Operations:")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")

        try:
            choice = int(input())
        except ValueError:
            print("Only enter a number 1-3")
            continue

        if choice == 1: # Add a new user
            print("Adding a new user!")
            user_mod.user_collection_add()
            break
        elif choice == 2: # View user details
            print("View single user details!")
            user_mod.view_user_details()
            break
        elif choice == 3: # Display all users
            print("Displaying all users:")
            user_mod.view_all_users()            
            break

def menu_author_ops():
    global author_collection
    while True:
        print("Author Operations:")
        print("1. Add a new author")
        print("2. View author details")
        print("3. Display all authors")

        try:
            choice = int(input())
        except ValueError:
            print("Only enter a number 1-3")
            continue

        if choice == 1: # Add a new author
            author_mod.author_collection_add()
            break
        elif choice == 2: # View author details
            author_mod.view_author_details()
            break
        elif choice == 3: # Display all authors
            print("Displaying all authors!")
            author_mod.view_all_authors()
            break

def menu_genre_ops():
    global genre_collection
    while True:
        print("Genre Operations:")
        print("1. Add a new genre")
        print("2. View genre details")
        print("3. Display all genres")

        try:
            choice = int(input())
        except ValueError:
            print("Only enter a number 1-3")
            continue

        if choice == 1: # Add a new genre
            print("Adding a new genre!")
            genre_mod.genre_collection_add()
            break
        elif choice == 2: # View genre details
            genre_mod.view_genre_details()
            break
        elif choice == 3: # Display all genres
            print("Displaying all genres!")
            genre_mod.view_all_genres()
            break


if __name__ == "__main__":
    main()