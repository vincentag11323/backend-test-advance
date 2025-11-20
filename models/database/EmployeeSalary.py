from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime  

class EmployeeSalary(SQLModel, table=True):
    """
    Schema for the table data to be stored in Database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_name: str = Field(index=True)
    annual_salary: float = Field(index=True)
    monthly_income_tax: float = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.now)


