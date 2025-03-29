import sqlite3
from models import create_table
from import_data import import_excel_to_db

def main():
    # Step 1: Create table
    print("Step 1: Creating table...")
    conn = sqlite3.connect('database.db')
    create_table(conn)
    conn.close()
    
    # Step 2: Import data
    print("\nStep 2: Importing data...")
    import_excel_to_db()

if __name__ == "__main__":
    main() 