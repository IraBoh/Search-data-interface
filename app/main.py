from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
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
    foreign_company: str = Query(None, description="Search in ForeignCompany field"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Results per page")
) -> Dict:
    # Create filters dictionary
    filters = {
        "Product": product,
        "IndianCompany": indian_company,
        "ForeignCompany": foreign_company
    }
    
    # Use the new multi_field_search method
    return data_service.multi_field_search(filters, page, page_size)

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