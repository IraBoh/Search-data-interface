# Indian Export Search - Technical Documentation

## Overview
A web application to search through Indian export data from June 2016, handling approximately 100,000 rows of data with potential for monthly additions.

## Architecture Decisions

### 1. Technology Stack
- **Backend: FastAPI (Python)**
  - Fast development with automatic API documentation
  - Built-in async support for better performance
  - Easy to extend with additional endpoints

- **Frontend: Mithril.js**
  - Lightweight (< 10KB) yet powerful
  - No build step needed
  - Simple to maintain and modify

- **Database: SQLite**
  - Self-contained, serverless
  - Zero configuration needed
  - Good for prototypes and medium datasets

### 2. Data Handling
Two approaches are implemented:

#### Excel Approach (`data_service.py`):
- Direct read using pandas
- Good for quick prototyping
- Limited by memory constraints
- Not suitable for multiple files

#### Database Approach (`db_service.py`):
- SQLite for structured storage
- Better for larger datasets
- Enables efficient querying
- Easier to add new data

### 3. Search Implementation
- Multi-field search across Product, IndianCompany, ForeignCompany
- Case-insensitive partial matching
- Pagination for large result sets

### 4. Containerization
- Docker for easy deployment
- Separate containers for frontend and backend
- Volume mounts for data persistence
- Hot-reload for development

## Current Limitations
1. **Data Growth**
   - Single file/month handling
   - No automated import process
   - Limited date-based filtering

2. **Performance**
   - Basic SQL queries without optimization
   - No caching implemented
   - Full table scans for searches

3. **Features**
   - Basic search functionality only
   - Limited filtering options
   - No export functionality

## Future Improvements

### Short Term
1. Add date-based filtering
2. Implement search result export
3. Add basic caching

### Long Term
1. **Data Growth Handling**
   - Automated import process
   - Better date partitioning
   - Archive system for old data

2. **Performance Optimization**
   - Implement proper indexing
   - Add caching layer
   - Query optimization

3. **Features**
   - Advanced filtering
   - Data visualization
   - Bulk export options

## Setup and Deployment
See README.md for setup instructions using Docker. 