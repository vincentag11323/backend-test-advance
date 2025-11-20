from typing import Union

from fastapi import FastAPI, HTTPException

from compute_tax import init_tax_system
from db import SessionDep, create_db_and_tables
from models import PostEmployeeSalary, EmployeeSalary, GetEmployeeSalaries
# from contextlib import asynccontextmanager
# import sqlite3   
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI(    
    title="Tax Calculator API",
    description="API to calculate tax liability using a progressive tax bracket system.")

DB_NAME = "tax_system.db"

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



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/employee_salaries/")
def calculate_and_create_employee_salary(employee_detail: PostEmployeeSalary, session : SessionDep):
    """calculates and saves newly created employee salary log into Database."""
    annual_salary_raw = employee_detail.annual_salary
    employee_name = employee_detail.employee_name

    # manual type checking and conversion to handle string income
    annual_salary: float
    if isinstance(annual_salary_raw, str):
        try:
            # Attempt to convert the string income to a float
            annual_salary = float(annual_salary_raw)
        except Exception as e:
            # If conversion fails (e.g., input is "not-a-number"), raise 400
            raise HTTPException(
                status_code=400,
                detail=f"Invalid annual_salary format for '{employee_name}'. annual_salary must be a numerical value, but received '{annual_salary_raw}'."
            )
    else:
        # if it was already a float, use it directly
        annual_salary = annual_salary_raw

    annual_tax:float = app.state.tax_system.compute_total_tax(annual_salary)
  
    # calculate gross monthly income and tax and net income
    gross_monthly_income = annual_salary / 12.0
    monthly_income_tax = annual_tax / 12.0
    net_monthly_income = gross_monthly_income - monthly_income_tax

    # store into DB
    new_employee_salary = EmployeeSalary(
        employee_name=employee_name,
        annual_salary=annual_salary,
        monthly_income_tax=monthly_income_tax
    )
    session.add(new_employee_salary)
    session.commit()
    session.refresh(new_employee_salary)

    # return the structured response
    # for readability purposes, format the salaries/income into string with 2 decimal places
    return {
        "employee_name": employee_name,
        "gross_monthly_income": f"{gross_monthly_income:.2f}", 
        "monthly_income_tax": f"{monthly_income_tax:.2f}",     
        "net_monthly_income": f"{net_monthly_income:.2f}",     
    }

@app.get("/employee_salaries/", response_model=GetEmployeeSalaries)
def get_employee_salaries(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> GetEmployeeSalaries:
    """retrieves all employee salaries from Database."""
    employee_salaries = session.exec(select(EmployeeSalary).offset(offset).limit(limit)).all()
    return  {
        "salary_computations": employee_salaries
    }
