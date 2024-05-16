
import book as book_mod
import user as user_mod
import author as author_mod
import genre as genre_mod

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