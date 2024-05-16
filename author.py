from database_connector import connect_db, close_connection
from mysql.connector import Error
    
def author_collection_add(name = ""):
    if not name:
        name = input("Enter the name of the new author: ")
    biography = input(f"Enter a biography for \'{name}\': ")
    conn, cursor = connect_db()
    if conn is not None:
        details = (name, biography)
        query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
        try:
            cursor.execute(query, details)
            conn.commit()
            print(f"{name} added to authors!")
        except Error as e:
            print("Problem adding author to database:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def view_author_details():
    conn, cursor = connect_db()
    if conn is not None:
        author_name = input("Enter the name of the author you would like to see the details of: ")
        author_name_lower = author_name.lower()
        lower_name_value = (author_name_lower,)
        query = "SELECT * FROM authors WHERE LOWER(name) LIKE %s"
        try:
            cursor.execute(query, lower_name_value)
            authors = cursor.fetchall()
        except Error as e:
            print("Issue viewing author details")
            print(f"Error: {e}")
        finally:
            if authors:
                print(f"Showing all authors with {author_name} in their name.")
                print("id|name|biography")
                for author in authors:
                    print(f"{author[0]}|{author[1]}|{author[2]}")
            else:
                print(f"No author with the name {author_name} found!")
            close_connection(conn, cursor)

def view_all_authors():
    conn, cursor = connect_db()
    if conn is not None:
        query = "SELECT * FROM authors"
        try:
            cursor.execute(query)
            authors = cursor.fetchall()
        except Error as e:
            print("Issue disaplying all authors!")
            print(f"Error: {e}")
        finally:
            if authors:
                print(f"Showing all authors.")
                print("id|name|biography")
                for author in authors:
                    print(f"{author[0]}|{author[1]}|{author[2]}")
            else:
                print("No authors yet!")
            close_connection(conn, cursor)

# Return boolean of if author name exists
def check_author_exists(author_name_lowered):
    conn, cursor = connect_db()
    if conn is not None:
        name_value = (author_name_lowered,)
        query = "SELECT * FROM authors WHERE LOWER(name) = %s"
        try:
            cursor.execute(query, name_value)
            results = cursor.fetchall()
        except Error as e:
            print("Issue checking if author exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(results)

# Input name, output id 
def get_author_id_by_name(author_name_lowered):
    conn, cursor = connect_db()
    if conn is not None:
        name_value = (author_name_lowered,)
        query = "SELECT * FROM authors WHERE LOWER(name) = %s"
        try:
            cursor.execute(query, name_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue checking if author exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return result[0]

# Input id, output name       
def get_author_name_by_id(author_id):
    conn, cursor = connect_db()
    if conn is not None:
        author_value = (author_id,)
        query = "SELECT name FROM authors WHERE id = %s"
        try:
            cursor.execute(query, author_value)
            author = cursor.fetchall()
            if author:
                close_connection(conn, cursor)
                return author[0][0]
        except Error as e:
            print("Problem finding author by id!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)