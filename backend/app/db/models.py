from sqlite3 import Connection

def create_table(conn: Connection):
    # First drop the existing table
    conn.execute('DROP TABLE IF EXISTS trade_data')
    
    # Then create new table with all TEXT fields
    conn.execute('''
    CREATE TABLE IF NOT EXISTS trade_data (
        -- Primary Key
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        -- 1. TRANSACTION DETAILS
        bill_no TEXT,
        date TEXT,
        invoice_no TEXT,
        item_no TEXT,
        
        -- 2. PRODUCT INFORMATION
        four_digit TEXT,
        hs_code TEXT,
        product TEXT,
        quantity TEXT,          -- Was REAL
        unit TEXT,
        item_rate_inv TEXT,     -- Was REAL
        item_rate_inr TEXT,     -- Was REAL
        
        -- 3. PRICING & CURRENCY
        currency TEXT,
        total_amount_inv_fc TEXT,  -- Was REAL
        fob_inr TEXT,           -- Was REAL
        
        -- 4. TRADE PARTIES
        indian_company TEXT,
        foreign_company TEXT,
        iec TEXT,
        iec_pin TEXT,
        cush TEXT,
        
        -- 5. LOCATION DETAILS
        foreign_port TEXT,
        foreign_country TEXT,
        indian_port TEXT,
        address1 TEXT,
        address2 TEXT,
        city TEXT
    )
    ''')
