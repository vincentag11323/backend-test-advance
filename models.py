from pydantic import BaseModel
from typing import Union, Optional

from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime  

class PostEmployeeSalary(BaseModel):
    """
    Schema for the income data received in the POST request body.
    """
    employee_name: str
    annual_salary: Union[float, str] #float may be represented in JSON as string

class EmployeeSalary(SQLModel, table=True):
    """
    Schema for the table data to be stored in Database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_name: str = Field(index=True)
    annual_salary: float = Field(index=True)
    monthly_income_tax: float = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.now)

class GetEmployeeSalaries(BaseModel):
    """
    Schema for the income data received in the GET request body.
    """
    salary_computations: list[EmployeeSalary]
