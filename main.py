
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
    # global book_collection
    # global user_collection
    # global author_collection
    # global genre_collection
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
            book_mod.borrow_book()
            break
        elif choice == 3: # Return a book
            book_returned_ISBN = input("Enter the ISBN of the book to return: ")
            try:
                book_to_return = book_collection[book_returned_ISBN]
            except KeyError:
                print("No book found with that ISBN!")
                continue

            book_collection[book_returned_ISBN], next_reserved_user_ID = book_to_return.return_book()
            print(f"{book_to_return.get_title()} returned!")
            if next_reserved_user_ID:
                next_user = user_collection[next_reserved_user_ID]
                user_mod.notify_user(next_user)
                book_collection[book_returned_ISBN] = book_collection[book_returned_ISBN].borrow_book(next_user.get_UUID())
                user_collection[next_reserved_user_ID] = next_user.add_to_borrow_history(book_collection[book_returned_ISBN])
                print(f"\'{book_to_return.get_title()}\' automatically lent out to user: {next_reserved_user_ID}.")
            save_books_file()
            save_users_file()
            break
        elif choice == 4: # Search for a book
            search = input("Enter part of the title of the book you would like to search: ")
            search_lower = search.lower()
            print(f"Here are all the books with {search} in the title:")
            book_counter = 0
            for book in book_collection.values():
                if search_lower in book.get_title().lower():
                    book_counter += 1
                    print(f"{book.get_title()}, {book.get_author()}, {book.get_ISBN()}, {book.get_genre()}, {book.get_publication_date()}, {book.get_available()}, Reservation List:{book.get_reserve_list()}")
            if book_counter == 0:
                print(f"No books found with \'{search}\' in the title!")                    
            break
        elif choice == 5: # Display all books
            print("Displaying all books in library:")
            for book in book_collection.values():
                print(f"{book.get_title()}, {book.get_author()}, {book.get_ISBN()}, {book.get_genre()}, {book.get_publication_date()}, {book.get_available()}, Reservation List:{book.get_reserve_list()}")
            break

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
            user_name = input("Enter the name of the new user: ")
            user_UUID = input(f"Declare a UUID for {user_name}: ")
            if user_collection:
                if user_UUID in user_collection:
                    print("There is already a user with that UUID! Please try again.")
                    break
            user_collection = user_mod.user_collection_add(user_name, user_UUID, user_collection)
            save_users_file()
            break
        elif choice == 2: # View user details
            user_ID = input("Enter the UUID of the user you wish to see details about: ")
            try:
                user_details = user_collection[user_ID]
            except:
                print(f"Could not find a user with the UUID of {user_ID}")
                break
            print(f"Details for user {user_ID}:")
            print(f"Name: {user_details.get_name()}")
            print(f"- Borrow History: {user_details.get_borrow_history()}")
            break
        elif choice == 3: # Display all users
            print("Displaying all users:")
            for user in user_collection.values():
                print(f"{user.get_UUID()}: {user.get_name()}")
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
            print("Adding a new author!")
            author_name = input("Enter the name of the new author: ")
            author_biography = input(f"Enter the biography of \'{author_name}\': ")
            author_collection = author_mod.author_collection_add(author_name, author_biography, author_collection)
            print(f"{author_name} added to Author collection!")
            save_authors_file()
            break
        elif choice == 2: # View author details
            author_name = input("Enter the name of the author you would like to see the details of: ")
            author_name_lower = author_name.lower()
            author_search = False

            # prints details for any author that has a matching string within
            for author in author_collection:
                if author_name_lower in author.get_name().lower():
                    author_search = True
                    print(f"{author.get_name()}'s biography:")
                    print(f"{author.get_biography()}")
            if not author_search:
                print(f"No author with the name {author_name} found!")

            break
        elif choice == 3: # Display all authors
            print("Displaying all authors!")
            for author in author_collection:
                print(f"{author.get_name()}'s biography: ")
                print(f"{author.get_biography()}")
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
            genre_name = input("Enter the name of the new genre: ")
            genre_list = [existing_genre.get_name().lower for existing_genre in genre_collection]
            if genre_name.lower() in genre_list:
                print(f"Genre {genre_name} already exists!")
                continue
            genre_description = input(f"Enter the description of \'{genre_name}\': ")
            genre_category = input(f"Enter the category of \'{genre_name}\': ")
            genre_collection = genre_mod.genre_collection_add(genre_name, genre_description, genre_category, genre_collection)
            print(f"{genre_name} added to Genre collection!")
            save_genres_file()
            break
        elif choice == 2: # View genre details
            genre_input = input("Enter the name of the Genre you would like to see details of: ")
            genre_lower = genre_input.lower()
            genre_search = False

            # prints details for any genre that has a matching string within
            for genre in genre_collection:
                if genre_lower in genre.get_name().lower():
                    genre_search = True
                    print(f"Genre: {genre.get_name()}")
                    print(f"- Description: {genre.get_description()}")
                    print(f"- Category: {genre.get_category()}")
            if not genre_search:
                print(f"No genre called {genre_input} found!")
            break
        elif choice == 3: # Display all genres
            print("Displaying all genres!")
            for genre in genre_collection:
                print(f"Genre: {genre.get_name()}")
                print(f"- Description: {genre.get_description()}")
                print(f"- Category: {genre.get_category()}")
            break


if __name__ == "__main__":
    main()