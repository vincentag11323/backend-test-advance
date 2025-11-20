from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import select
from compute_tax import TaxBracketComposite
from models.database.EmployeeSalary import EmployeeSalary
from models.validators.GetEmployeeSalaries import GetEmployeeSalaries
from models.validators.PostEmployeeSalary import PostEmployeeSalary
from db import SessionDep

employee_salaries_router = APIRouter(
    prefix="/employee_salaries", 
    tags=["Employee Salaries"]
)

# --- Dependency Definition ---
def get_tax_system(request: Request) -> TaxBracketComposite:
    return request.app.state.tax_system

TaxSystemDep = Annotated[TaxBracketComposite, Depends(get_tax_system)] 

@employee_salaries_router.post("/")
def calculate_and_create_employee_salary(
    employee_detail: PostEmployeeSalary, 
    tax_system: TaxSystemDep,
    session : SessionDep # db session
    ):
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

    annual_tax:float = tax_system.compute_total_tax(annual_salary)
  
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

@employee_salaries_router.get("/", response_model=GetEmployeeSalaries)
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
