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
    def multi_field_search(self, filters: Dict[str, str]) -> Dict:
        """
        Search with multiple field conditions
        Args:
            filters: Dictionary of field-query pairs
                Example: {"Product": "cotton", "ForeignCompany": "plastic"}
        """
        if self.df is None:
            return {"total_matches": 0, "results": []}

        results = self.df.copy()
        
        for field, query in filters.items():
            if query:
                results = results[results[field].str.contains(query, case=False, na=False)]
        
        records = results.head(10).to_dict('records')

        return {
            "searches": filters,
            "total_matches": len(results),
            "showing": min(10, len(results)),
            "results": {f"Result {i+1}": r for i, r in enumerate(records)}
        }

# Test the class
if __name__ == "__main__":
    service = DataService()
    
    # Test multi-field search
    test_filters = {
        "Product": "cotton",
        "ForeignCompany": "plastic"
    }
    results = service.multi_field_search(test_filters)
    print(f"Found {results['total_matches']} matches")