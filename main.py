from fastapi import FastAPI
from compute_tax import init_tax_system
from db import create_db_and_tables
from routes.employee_salaries_router import employee_salaries_router

app = FastAPI(    
    title="Tax Calculator API",
    description="API to calculate tax liability using a progressive tax bracket system.")

app.include_router(employee_salaries_router)

@app.on_event("startup")
async def initialize_tax_system():
    """
    Initializes the composite structure ONCE when the application starts.
    Stores the instance in the app.state object for easy access in endpoints.
    """
    print("Initializing Tax System Composite...")
    
    # Store the initialized system in the application state
    app.state.tax_system = init_tax_system()
    print("Tax System Composite initialized and ready.")

@app.on_event("startup")
def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    create_db_and_tables()


# display sample Hello World at root.
@app.get("/")
def read_root():
    return {"Hello": "World"}


