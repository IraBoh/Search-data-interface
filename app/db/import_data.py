import pandas as pd
import sqlite3
from pathlib import Path

def import_excel_to_db():
    try:
        # Get the current file's directory (app/db folder)
        current_dir = Path(__file__).parent
        db_path = current_dir / 'database.db'
        
        print(f"Using database at: {db_path}")
        
        # Connect to database with absolute path
        conn = sqlite3.connect(db_path)
        
        # Read Excel file
        excel_path = Path(r"C:\Users\Bruger\Documents\Programming\isynet-search-data\data\IMEX-IN-2016-06-EX.part2.xlsx")
        
        print(f"Looking for Excel file at: {excel_path}")
        df = pd.read_excel(excel_path)
        
        print("Original columns:", df.columns.tolist())
        
        # Convert ALL columns to strings (not just numeric ones)
        for column in df.columns:
            df[column] = df[column].astype(str)
        
        print("All columns converted to string")
        
        # Rename columns to match database
        column_mapping = {
            'BillNO': 'bill_no',
            '4Digit': 'four_digit',
            'Date': 'date',
            'HSCode': 'hs_code',
            'Product': 'product',
            'Quantity': 'quantity',
            'Unit': 'unit',
            'Item_Rate_INV': 'item_rate_inv',
            'Currency': 'currency',
            'Total_Amount_INV_FC': 'total_amount_inv_fc',
            'FOB INR': 'fob_inr',
            'ForeignPort': 'foreign_port',
            'ForeignCountry': 'foreign_country',
            'IndianPort': 'indian_port',
            'IEC': 'iec',
            'IndianCompany': 'indian_company',
            'Address1': 'address1',
            'Address2': 'address2',
            'City': 'city',
            'ForeignCompany': 'foreign_company',
            'Invoice_No': 'invoice_no',
            'CUSH': 'cush',
            'IEC_PIN': 'iec_pin',
            'Item_No': 'item_no',
            'Item_Rate_INR': 'item_rate_inr'
        }
        
        df = df.rename(columns=column_mapping)
        print("Final columns:", df.columns.tolist())
        
        # Force SQLite to use TEXT for all columns during import
        df.to_sql('trade_data', conn, if_exists='replace', index=False, dtype={col: 'TEXT' for col in df.columns})
        
        print(f"Successfully imported {len(df)} rows!")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    import_excel_to_db() 