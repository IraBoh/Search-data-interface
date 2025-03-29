# app/db/test_sqlite.py
import sqlite3
import os

try:
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create database path in the same directory as this script
    db_path = os.path.join(current_dir, 'database.db')
    
    # Create connection
    conn = sqlite3.connect(db_path)
    print(f"SQLite connection successful!")
    print(f"Database created at: {db_path}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
