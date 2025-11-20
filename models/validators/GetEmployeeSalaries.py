from pydantic import BaseModel
from models.database.EmployeeSalary import EmployeeSalary

class GetEmployeeSalaries(BaseModel):
    """
    Schema for the income data received in the GET request body.
    """
    salary_computations: list[EmployeeSalary]
