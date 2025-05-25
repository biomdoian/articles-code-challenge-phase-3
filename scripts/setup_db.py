import sqlite3
from lib.db.connection import get_connection # Import the get_connection function

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()

   