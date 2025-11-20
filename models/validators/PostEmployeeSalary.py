from pydantic import BaseModel
from typing import Union

class PostEmployeeSalary(BaseModel):
    """
    Schema for the income data received in the POST request body.
    """
    employee_name: str
    annual_salary: Union[float, str] #float may be represented in JSON as string
