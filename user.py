from database_connector import connect_db, close_connection
from mysql.connector import Error
    
def user_collection_add():
    conn, cursor = connect_db()
    if conn is not None:
        name = input("Enter the name of the new user: ")
        while True:
            # Validating library id length and unqiueness
            library_id = input("Enter a unique 10 cahracter library id for the new user: ")
            if len(library_id) != 10:
                print("Library_id has to be exactly 10 characters!")
                continue
            if check_user_exists_by_library_id(library_id):
                print("User already exists with that library_id. Please choose another!")
                continue
            break
        user_values = (name, library_id)
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        cursor.execute(query, user_values)
        conn.commit()
        print("New user added!")
        close_connection(conn, cursor)

def view_user_details():
    conn, cursor = connect_db()
    if conn is not None:
        while True:
            # Validating library id length and existence
            library_id = input("Enter the library_id of user you want to view details of: ")
            if len(library_id) != 10:
                print("Library_id has to be exactly 10 characters!")
                continue
            if check_user_exists_by_library_id(library_id):
                break
            else:
                print(f"No user found with library id of \'{library_id}\'")
                continue
        library_id_value = (library_id,)
        query = "SELECT * FROM users WHERE library_id = %s"
        try:
            cursor.execute(query, library_id_value)
            user = cursor.fetchone()
        except Error as e:
            print("Problem viewing user details!")
            print(f"Error: {e}")
        finally:
            if user:
                print("id|name|library_id")
                print(f"{user[0]}|{user[1]}|{user[2]}")
            close_connection(conn, cursor)

def view_all_users():
    conn, cursor = connect_db()
    if conn is not None:        
        query = "SELECT * FROM users"
        try:
            cursor.execute(query)
            user_list = cursor.fetchall()
        except Error as e:
            print("Issue displaying all users!")
            print(f"Error: {e}")
        finally:
            if user_list:
                print("id|name|library_id")
                for user in user_list:
                    print(f"{user[0]}|{user[1]}|{user[2]}")
            close_connection(conn, cursor)

# Return boolean if user with input 'id' exists
def check_user_exists(user_id):
    conn, cursor = connect_db()
    if conn is not None:
        id_value = (user_id,)
        query = "SELECT * FROM users WHERE id = %s"
        try:
            cursor.execute(query, id_value)
            results = cursor.fetchone()
        except Error as e:
            print("Issue checking if user exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(results)

# Return boolean if user with input 'library_id' exists
def check_user_exists_by_library_id(library_id):
    conn, cursor = connect_db()
    if conn is not None:
        library_id_value = (library_id,)
        query = "SELECT * FROM users WHERE library_id = %s"
        try:
            cursor.execute(query, library_id_value)
            results = cursor.fetchone()
        except Error as e:
            print("Issue checking if user exists:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return bool(results)

# Input libaray_id, output id
def get_id_by_library_id(library_id):
    conn, cursor = connect_db()
    if conn is not None:
        library_id_value = (library_id,)
        query = "SELECT id from users WHERE library_id = %s"
        try:
            cursor.execute(query, library_id_value)
            result = cursor.fetchone()
        except Error as e:
            print("Issue finding user.id by library_id!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
        if result:
            return result[0]

# Return a list of book ids borrowed by a user        
def get_user_borrowed_books_by_library_id(library_id):
    conn, cursor = connect_db()
    user_id = get_id_by_library_id(library_id)
    if conn is not None:
        user_value = (user_id,)
        query = "SELECT * FROM borrowed_books WHERE user_id = %s"
        try:
            cursor.execute(query, user_value)
        except Error as e:
            print(f"Problem getting list of books borrwed by user \'{library_id}\'!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)
            return cursor.fetchall()

# potentially send email or something
def notify_user(user):
    pass