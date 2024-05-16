from database_connector import connect_db, close_connection
from mysql.connector import Error
    
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
        
def get_author_name_by_id(author_id):
    conn, cursor = connect_db()
    if conn is not None:
        query = f"SELECT name FROM authors WHERE id = {author_id}"
        try:
            cursor.execute(query)
            author = cursor.fetchone()
            return author[0]
        except Error as e:
            print("Problem finding author by id!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)