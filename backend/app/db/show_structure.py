import sqlite3
from pathlib import Path

def show_db_structure():
    db_path = Path(__file__).parent / 'database.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nDatabase Structure for trade_data table:")
    print("=" * 50)
    
    # Get column info
    cursor.execute("PRAGMA table_info(trade_data)")
    columns = cursor.fetchall()
    
    # Group definitions
    groups = {
        "PRIMARY KEY": ["id"],
        "1. TRANSACTION DETAILS": ["bill_no", "date", "invoice_no", "item_no"],
        "2. PRODUCT INFORMATION": ["four_digit", "hs_code", "product", "quantity", "unit", "item_rate_inv", "item_rate_inr"],
        "3. PRICING & CURRENCY": ["currency", "total_amount_inv_fc", "fob_inr"],
        "4. TRADE PARTIES": ["indian_company", "foreign_company", "iec", "iec_pin", "cush"],
        "5. LOCATION DETAILS": ["foreign_port", "foreign_country", "indian_port", "address1", "address2", "city"]
    }
    
    # Show structure by group
    for group_name, group_columns in groups.items():
        print(f"\n{group_name}:")
        print("-" * 30)
        for col in columns:
            if col[1] in group_columns:  # col[1] is column name
                print(f"Column: {col[1]:<20} Type: {col[2]:<10}")
    
    conn.close()

if __name__ == "__main__":
    show_db_structure() 