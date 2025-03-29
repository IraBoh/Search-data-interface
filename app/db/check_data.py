import sqlite3
from pathlib import Path

def check_imported_data():
    # Use same path as import script
    db_path = Path(__file__).parent / 'database.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nChecking imported data:")
    print("=" * 50)
    
    # 1. Count total rows
    cursor.execute("SELECT COUNT(*) FROM trade_data")
    total_rows = cursor.fetchone()[0]
    print(f"\n1. Total rows in database: {total_rows}")
    
    # 2. Show sample data
    print("\n2. Sample of first 3 rows:")
    cursor.execute("""
        SELECT 
            bill_no,
            date,
            product,
            quantity,
            fob_inr,
            indian_company
        FROM trade_data 
        LIMIT 3
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"\nBill: {row[0]}")
        print(f"Date: {row[1]}")
        print(f"Product: {row[2]}")
        print(f"Quantity: {row[3]}")
        print(f"FOB INR: {row[4]}")
        print(f"Company: {row[5]}")
    
    conn.close()

if __name__ == "__main__":
    check_imported_data() 