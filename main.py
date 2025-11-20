from fastapi import FastAPI
from compute_tax import init_tax_system
from db import create_db_and_tables
from routes.employee_salaries_router import employee_salaries_router

app = FastAPI(    
    title="Tax Calculator API",
    description="API to calculate tax liability using a progressive tax bracket system.")

app.include_router(employee_salaries_router)

@app.on_event("startup")
def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    create_db_and_tables()


# display sample Hello World at root.
@app.get("/")
def read_root():
    return {"Hello": "World"}