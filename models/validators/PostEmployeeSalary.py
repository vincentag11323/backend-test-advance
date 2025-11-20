from pydantic import BaseModel, Field, field_validator
from typing import Any, Union

class PostEmployeeSalary(BaseModel):
    """
    Schema for the income data received in the POST request body.
    """
    employee_name: str = Field(min_length=1, description="The employee's full name must be at least 1 character long.")
    annual_salary: Union[float, str] = Field(gt=0, description="The annual salary must be greater than 0.") #float may be represented in JSON as string
    @field_validator('annual_salary', mode='before')
    @classmethod
    def convert_salary_to_float(cls, value: Union[str, float, Any]) -> float:
        if isinstance(value, str):
            try:
                # basic conversion
                return float(value)
            except ValueError:
                # Pydantic will report the ValueError to the user
                raise ValueError("Annual salary must be a valid number.")
        
        # if the input is already a number (float or int), return it.
        # this handles the case where float is passed directly in JSON.
        if isinstance(value, (int, float)):
            return value
        
        # if it's anything else, let Pydantic handle the type error.
        return value