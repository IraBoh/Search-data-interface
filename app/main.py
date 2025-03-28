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
    results = []
    total_matches = 0
    
    # Search in each field if query provided
    if product:
        product_results = data_service.search(query=product, field="Product")
        results.extend(product_results["results"])
        total_matches += product_results["total_matches"]
        
    if indian_company:
        indian_results = data_service.search(query=indian_company, field="IndianCompany")
        results.extend(indian_results["results"])
        total_matches += indian_results["total_matches"]
        
    if foreign_company:
        foreign_results = data_service.search(query=foreign_company, field="ForeignCompany")
        results.extend(foreign_results["results"])
        total_matches += foreign_results["total_matches"]
    
    # Remove duplicates and limit results
    unique_results = list({str(r): r for r in results}.values())[:10]
    
    return {
        "searches": {
            "product": product,
            "indian_company": indian_company,
            "foreign_company": foreign_company
        },
        "total_matches": total_matches,
        "showing": len(unique_results),
        "results": {f"Result {i+1}": r for i, r in enumerate(unique_results)}
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