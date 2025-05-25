from lib.db.connection import get_connection
#from lib.models.author import Author
# from lib.models.magazine import Magazine
# from lib.models.article import Article
def debug_cli():
    print("Welcome to the Debug CLI!")
    conn = get_connection()
    cursor = conn.cursor()

    #check if the tables exist
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in the database:{[t['name']for t in tables]}")
    except Exception as e:
        print(f"Error checking tables: {e}")
    conn.close()

print("Exiting Debug CLI.")
if __name__ == "__main__":
    debug_cli()
# This script is a simple CLI for debugging the database connection and checking tables.
        