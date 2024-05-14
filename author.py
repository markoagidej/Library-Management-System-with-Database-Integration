from database_connector import connect_db, close_connection
from mysql.connector import Error

# class Author:
#     def __init__(self, name, biography):
#         self.__name = name
#         self.__biography = biography

#     def get_name(self):
#         return self.__name

#     def get_biography(self):
#         return self.__biography

#     def __str__(self):
#         return self.__name
    
def author_collection_add(name = ""):
    if not name:
        name = input(input("Enter the name of the new author: "))
    biography = input(f"Enter a biography for \'{name}\': ")
    conn, cursor = connect_db()
    if conn is not None:
        details = (name, biography)
        query = "INSERT INTO auhtors (name, biography) VALUES (%s, %s)"
        try:
            cursor.execute(query, details)
            conn.commit()
            print(f"{name} added to authors!")
        except Error as e:
            print("Problem adding author to database:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

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