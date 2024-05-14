from database_connector import connect_db, close_connection
from mysql.connector import Error

# class Genre:
#     def __init__(self, name, description, category):
#         self.__name = name
#         self.__description = description
#         self.__category = category

#     def get_name(self):
#         return self.__name

#     def get_description(self):
#         return self.__description

#     def get_category(self):
#         return self.__category
    
#     def __str__(self):
#         return self.__name
    
def genre_collection_add(name = ""):
    if not name:
        name = input(input("Enter the name of the new genre: "))
    description = input(f"Enter a description for \'{name}\': ")
    conn, cursor = connect_db()
    if conn is not None:
        details = (name, description)
        query = "INSERT INTO genres (name, description) VALUES (%s, %s)"
        try:
            cursor.execute(query, details)
            conn.commit()
            print(f"{name} added to genres!")
        except Error as e:
            print("Problem adding genre to database:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def check_genre_exists(genre_name_lowered):
    conn, cursor = connect_db()
    if conn is not None:
        name_value = (genre_name_lowered,)
        query = "SELECT * FROM genres WHERE LOWER(name) = %s"
        try:
            cursor.execute(query, name_value)
            results = cursor.fetchall()
        except Error as e:
            print("Issue checking if genre exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(results)
        
def get_genre_id_by_name(genre_name_lowered):
    conn, cursor = connect_db()
    if conn is not None:
        name_value = (genre_name_lowered,)
        query = "SELECT * FROM genres WHERE LOWER(name) = %s"
        try:
            cursor.execute(query, name_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue checking if genre exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return result[0]