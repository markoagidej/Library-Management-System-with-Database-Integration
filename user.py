from database_connector import connect_db, close_connection
from mysql.connector import Error

# class User:
#     def __init__(self, name, library_uuid):
#         self.__name = name
#         self.__library_uuid = library_uuid

#     def get_name(self):
#         return self.__name

#     def get_library_uuid(self):
#         return self.__library_uuid
    
def user_collection_add(name, library_uuid, collection):
    new_user = User(name, library_uuid)
    if collection:
        collection[library_uuid] = new_user
    else:
        collection = {library_uuid: new_user}
    return collection

def check_user_exists(user_id):
    conn, cursor = connect_db()
    if conn is not None:
        name_value = (user_id,)
        query = "SELECT * FROM users WHERE LOWER(name) = %s"
        try:
            cursor.execute(query, name_value)
            results = cursor.fetchall()
        except Error as e:
            print("Issue checking if user exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(results)
                
# Return a list of book ids borrowed by a user        
def get_user_borrowed_books(user_id):
    conn, cursor = connect_db()
    if conn is not None:
        user_value = (user_id,)
        query = "SELECT * FROM borrowed_books WHERE user_id = %s"
        try:
            cursor.execute(query, user_value)
        except Error as e:
            print(f"Problem getting list of books borrwed by user \'{user_id}\'!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return cursor.fetchall()


def notify_user(user):
    # potentially send email or something
    pass