from database_connector import connect_db, close_connection
from mysql.connector import Error
    
def genre_collection_add(name = ""):
    if not name:
        name = input(input("Enter the name of the new genre: "))
    description = input(f"Enter a description for \'{name}\': ")
    category = input(f"Enter a category for \'{name}\': ")
    conn, cursor = connect_db()
    if conn is not None:
        details = (name, description, category)
        query = "INSERT INTO genres (name, description, category) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, details)
            conn.commit()
            print(f"{name} added to genres!")
        except Error as e:
            print("Problem adding genre to database:")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)

def view_genre_details():
    conn, cursor = connect_db()
    if conn is not None:
        genre_name = input("Enter the name of the genre you would like to see the details of: ")
        genre_name_lower = genre_name.lower()
        lower_name_value = (genre_name_lower,)
        query = "SELECT * FROM genres WHERE LOWER(name) LIKE %s"
        try:
            cursor.execute(query, lower_name_value)
            genres = cursor.fetchall()
        except Error as e:
            print("Issue viewing genre details")
            print(f"Error: {e}")
        finally:
            if genres:
                print(f"Showing all genres with {genre_name} in their name.")
                print("id|name|description|category")
                for genre in genres:
                    print(f"{genre[0]}|{genre[1]}|{genre[2]}|{genre[3]}")
            else:
                print(f"No genre with the name {genre_name} found!")
            close_connection(conn, cursor)

def view_all_genres():
    conn, cursor = connect_db()
    if conn is not None:
        query = "SELECT * FROM genres"
        try:
            cursor.execute(query)
            genres = cursor.fetchall()
        except Error as e:
            print("Issue disaplying all genres!")
            print(f"Error: {e}")
        finally:
            if genres:
                print(f"Showing all genres.")
                print("id|name|description|category")
                for genre in genres:
                    print(f"{genre[0]}|{genre[1]}|{genre[2]}|{genre[3]}")
            else:
                print("No authors yet!")
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
        
def get_genre_name_by_id(genre_id):    
    conn, cursor = connect_db()
    if conn is not None:
        query = f"SELECT name FROM genres WHERE id = {genre_id}"
        try:
            cursor.execute(query)
            genre = cursor.fetchone()
            return genre[0]
        except Error as e:
            print("Problem finding genre by id!")
            print(f"Error: {e}")
        finally:
            close_connection(conn, cursor)