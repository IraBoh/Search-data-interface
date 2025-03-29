import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

class DBService:    # Changed class name too
    def __init__(self):
        self.db_path = Path(__file__).parent / 'db' / 'database.db'
        
    def get_connection(self):
        """Get SQLite connection with row factory for dict results"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def multi_field_search(self, filters: Dict[str, str], page: int = 1, page_size: int = 10) -> Dict:
        """
        Search with multiple field conditions
        Args:
            filters: Dictionary of field-query pairs
                Example: {"product": "cotton", "foreign_company": "plastic"}
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build the WHERE clause dynamically
            where_clauses = []
            params = []
            for field, query in filters.items():
                if query:
                    # Convert PascalCase to snake_case for database query
                    db_field = field.lower()  # Convert Product to product
                    where_clauses.append(f"{db_field} LIKE ?")
                    params.append(f"%{query}%")
            
            # Construct the full query
            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            # Get total matches
            count_sql = f"SELECT COUNT(*) FROM trade_data WHERE {where_sql}"
            cursor.execute(count_sql, params)
            total_matches = cursor.fetchone()[0]
            
            # Get paginated results
            offset = (page - 1) * page_size
            results_sql = f"""
                SELECT * FROM trade_data 
                WHERE {where_sql}
                LIMIT ? OFFSET ?
            """
            cursor.execute(results_sql, params + [page_size, offset])
            
            # Convert results to list of dicts with PascalCase keys
            results = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                formatted_row = {
                    "BillNO": row_dict["bill_no"],
                    "Date": row_dict["date"],
                    "Product": row_dict["product"],
                    "IndianCompany": row_dict["indian_company"],
                    "ForeignCompany": row_dict["foreign_company"],
                    "Quantity": row_dict["quantity"],
                    "Unit": row_dict["unit"],
                    "Item_Rate_INV": row_dict["item_rate_inv"],
                    "Item_Rate_INR": row_dict["item_rate_inr"],
                    "Currency": row_dict["currency"],
                    "Total_Amount_INV_FC": row_dict["total_amount_inv_fc"],
                    "FOB_INR": row_dict["fob_inr"],
                    "IEC": row_dict["iec"],
                    "4Digit": row_dict["four_digit"],
                    "HSCode": row_dict["hs_code"],
                    # Add other fields as needed...
                }
                results.append(formatted_row)
            
            return {
                "searches": filters,
                "total_matches": total_matches,
                "page": page,
                "page_size": page_size,
                "has_more": (offset + page_size) < total_matches,
                "results": results
            }
            
        except Exception as e:
            print(f"Search error: {e}")
            return {"total_matches": 0, "results": []}
            
        finally:
            conn.close()

# Test the class
if __name__ == "__main__":
    service = DBService()    # Updated class name in test
    
    # Test multi-field search
    test_filters = {
        "product": "cotton",
        "foreign_company": "plastic"
    }
    results = service.multi_field_search(test_filters)
    print(f"Found {results['total_matches']} matches")
    if results['results']:
        print("\nFirst result:")
        for key, value in results['results'][0].items():
            print(f"{key}: {value}") 