# Indian Export Search

Web application for searching Indian export data from June 2016.

## Features
- Search by Product, Indian Company, or Foreign Company
- Display search results in a table
- Handle large Excel datasets
- Docker containerization

## Requirements
- Docker Desktop

## How to Run
1. Install and start Docker Desktop
2. Clone this repository
3. In the project directory, run:
   
   docker-compose up --build

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Technologies
- Backend: FastAPI (Python)
- Frontend: Mithril.js
- Database: SQLite
- Containerization: Docker