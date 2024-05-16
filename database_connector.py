import mysql.connector
from mysql.connector import Error

# Connect to DB and return the connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            database="applying_sql_in_python",
            user="root",
            password="PASSWORD",
            host="localhost"
            )
        if conn.is_connected():
            cursor = conn.cursor()
            return conn, cursor
    except Error as e:
        print("Problem connection to server.")
        print(f"Error: {e}")
        return None, None
    
# close the assumed opne connection and cursor
def close_connection(connection, cursor):
    cursor.close()
    connection.close()