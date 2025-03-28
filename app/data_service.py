import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional

class DataService:
    def __init__(self):
        self.df = None
        self.load_data()

    def load_data(self):
        """Load the Excel file into a pandas DataFrame"""
        # Using pathlib for better path handling
        file_path = Path("data/IMEX-IN-2016-06-EX.part2.xlsx")
        
        try:
            self.df = pd.read_excel(file_path)
            print("Data loaded successfully!")  # Simplified
            print(f"Total rows: {len(self.df)}")  # Only show total rows
            
        except Exception as e:
            print(f"Error loading data: {e}")

    def search(self, query: str, field: str = "Product", limit: int = 10) -> Dict:
        """
        Search the DataFrame for matching records
        Args:
            query (str): The search term
            field (str): Field to search in
            limit (int): Maximum number of results to return
        """
        if self.df is None:
            return {"total_matches": 0, "results": []}
        
        # Case-insensitive search
        mask = self.df[field].str.contains(query, case=False, na=False)
        results = self.df[mask]
        
        # Get total matches before limiting
        total_matches = len(results)
        
        # Select fields and limit results
        selected_fields = [
            'Date', 'Product', 'IndianCompany', 'ForeignCompany',
            'ForeignCountry', 'Quantity', 'Unit', 'Total_Amount_INV_FC',
            'ForeignPort'
        ]
        
        # Convert to records first, then wrap in response dict
        records = results[selected_fields].head(limit).to_dict('records')
        
        return {
            "total_matches": total_matches,
            "results": records
        }

# Test the class
if __name__ == "__main__":
    # Single instance
    service = DataService()
    
    # Get results once
    results = service.search("steel")
    
    # Print header
    print("\n" + "="*50)
    print(f"Search results for 'steel' (Found: {results['total_matches']})")
    print("="*50)
    
    # Single print loop
    for idx, r in enumerate(results['results'], 1):
        print(f"\nResult {idx}:")
        print("-"*40)
        # Print each field exactly once in fixed order
        fields_to_print = [
            ('Date', lambda x: x.strftime('%Y-%m-%d')),
            ('Product', str),
            ('IndianCompany', str),
            ('ForeignCompany', str),
            ('ForeignCountry', str),
            ('Quantity', str),
            ('Unit', str),
            ('Total_Amount_INV_FC', str),
            ('ForeignPort', str)
        ]
        
        for field, formatter in fields_to_print:
            value = r.get(field)
            if value is not None:
                print(f"{field}: {formatter(value)}")
    
    # Clear end marker
    print("\n" + "="*50)
    print("END OF RESULTS")
    print("="*50 + "\n")