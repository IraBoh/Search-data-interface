from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from .data_service import DataService  # Add dot for relative import
from .db_service import DBService     # Add dot for relative import

app = FastAPI(title="Indian Export Search API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize both services
data_service = DataService()  # Excel service
db_service = DBService()      # DB service

@app.get("/search/")  # Excel-based endpoint
async def search(
    product: str = Query(None, description="Search in Product field"),
    indian_company: str = Query(None, description="Search in IndianCompany field"),
    foreign_company: str = Query(None, description="Search in ForeignCompany field"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Results per page")
) -> Dict:
    filters = {
        "Product": product,
        "IndianCompany": indian_company,
        "ForeignCompany": foreign_company
    }
    return data_service.multi_field_search(filters, page, page_size)

@app.get("/db-search/")  # DB-based endpoint
async def db_search(
    product: str = Query(None, description="Search in Product field"),
    indian_company: str = Query(None, description="Search in IndianCompany field"),
    foreign_company: str = Query(None, description="Search in ForeignCompany field"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Results per page")
) -> Dict:
    filters = {
        "product": product,
        "indian_company": indian_company,
        "foreign_company": foreign_company
    }
    return db_service.multi_field_search(filters, page, page_size)

@app.get("/")
async def root():
    return {
        "message": "Indian Export Search API",
        "version": "1.0",
        "endpoints": {
            "excel_search": "/search/?query=<term>&field=<field>",
            "db_search": "/db-search/?query=<term>&field=<field>"
        }
    }