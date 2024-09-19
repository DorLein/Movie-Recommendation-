import sqlite3

DATABASE = 'User.db'

def execute_query(query, params=()):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()

def create_tables():
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """
    create_newsletter_table = """
    CREATE TABLE IF NOT EXISTS newsletter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL
    );
    """
    execute_query(create_users_table)
    execute_query(create_newsletter_table)

if __name__ == "__main__":
    create_tables()
