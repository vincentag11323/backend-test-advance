from fastapi import APIRouter
from sqlmodel import select
from compute_tax import init_tax_system
from models.database.EmployeeSalary import EmployeeSalary
from models.validators.GetEmployeeSalaries import GetEmployeeSalaries
from models.validators.PostEmployeeSalary import PostEmployeeSalary
from db import SessionDep

employee_salaries_router = APIRouter(
    prefix="/employee_salaries", 
    tags=["Employee Salaries"]
)

@employee_salaries_router.post("/")
def calculate_and_create_employee_salary(
    employee_detail: PostEmployeeSalary, 
    session : SessionDep # db session
    ):
    """calculates and saves newly created employee salary log into Database."""
    annual_salary = employee_detail.annual_salary
    employee_name = employee_detail.employee_name

    # init tax_system
    tax_system = init_tax_system()
    # compute tax
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
