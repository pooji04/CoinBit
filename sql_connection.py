import mysql.connector as mysql

def create_sql_connection():
    return mysql.connect(
        host='localhost',
        user='root',
        password='poojitha',
        database='coinbit'
    )

def create_sql_cursor(connection):
    return connection.cursor()

def close_connection(connection, cursor):
    cursor.close()
    connection.close()
