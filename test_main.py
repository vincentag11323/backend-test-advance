from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_employee_salary_negative_number():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={"employee_name": "gilbert", "annual_salary": "-5"},
    )
    assert response.status_code == 422
    assert len(response.json()['detail']) > 0
    assert response.json()['detail'][0]['msg'] == "Input should be greater than 0"
       
def test_create_employee_salary_string_salary_empty():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={"employee_name": "gilbert", "annual_salary": ""},
    )
    assert response.status_code == 422
    assert len(response.json()['detail']) > 0
    assert response.json()['detail'][0]['msg'] == "Value error, Annual salary must be a valid number."
           
def test_create_employee_salary_string_salary_non_number():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={"employee_name": "gilbert", "annual_salary": "asd"},
    )
    assert response.status_code == 422
    assert len(response.json()['detail']) > 0
    assert response.json()['detail'][0]['msg'] == "Value error, Annual salary must be a valid number."
           
def test_create_employee_salary_string_salary_valid():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={"employee_name": "gilbert", "annual_salary": "60000"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "employee_name": "gilbert",
        "gross_monthly_income": "5000.00",
        "monthly_income_tax": "500.00",
        "net_monthly_income": "4500.00"
    }

def test_create_employee_salary_invalid_name():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={"employee_name": 123,"annual_salary": 60000},
    )
    assert response.status_code == 422
    assert len(response.json()['detail']) > 0
    assert response.json()['detail'][0]['msg'] == "Input should be a valid string"

def test_create_employee_salary_empty_body():
    response = client.post(
        "/employee_salaries/",
        headers={},
        json={},
    )
    assert response.status_code == 422
    assert len(response.json()['detail']) > 1
    assert response.json()['detail'][0]['msg'] == "Field required"
    assert response.json()['detail'][1]['msg'] == "Field required"