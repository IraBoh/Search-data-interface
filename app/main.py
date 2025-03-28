from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from .data_service import DataService

app = FastAPI(title="Indian Export Search API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DataService
data_service = DataService()

@app.get("/search/")
async def search(
    product: str = Query(None, description="Search in Product field"),
    indian_company: str = Query(None, description="Search in IndianCompany field"),
    foreign_company: str = Query(None, description="Search in ForeignCompany field")
) -> Dict:
    # Start with all results
    results = data_service.df
    total_matches = 0
    
    # Apply each filter if provided
    if product:
        results = results[results['Product'].str.contains(product, case=False, na=False)]
        
    if indian_company:
        results = results[results['IndianCompany'].str.contains(indian_company, case=False, na=False)]
        
    if foreign_company:
        results = results[results['ForeignCompany'].str.contains(foreign_company, case=False, na=False)]
    
    # Get total matches after all filters
    total_matches = len(results)
    
    # Convert to records (limit to 10)
    records = results.head(10).to_dict('records')
    
    return {
        "searches": {
            "product": product,
            "indian_company": indian_company,
            "foreign_company": foreign_company
        },
        "total_matches": total_matches,
        "showing": len(records),
        "results": {f"Result {i+1}": r for i, r in enumerate(records)}
    }

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Indian Export Search API",
        "version": "1.0",
        "endpoints": {
            "search": "/search/?query=<term>&field=<field>"
        }
    }