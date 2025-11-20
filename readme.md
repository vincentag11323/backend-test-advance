# Introduction
I've written the solutions in Python language with FASTAPI framework.
Python have classes and allow inheritances for OOP , but not implementations and interface (unlike java).
For the OOP Design Pattern, I've done `Template Method pattern` as well as `Composite pattern`, 
For further details on Design Pattern, I've attached UML diagrams to list all my implementations.
I've written the API with FASTAPI framework.

# Server
```
Server starts at http://127.0.0.1:8000
Server Documentation at http://127.0.0.1:8000/docs  
```
Documentation is using Swagger UI. FASTAPI autogenerates this by default.

# APIs
There's 3 APIs written:

- `/` returns Hello World
- GET `/employee_salaries` to get all salaries stored in database.
- POST `/employee_salaries` with employee name and salary amount to store into database.

# Pre-requisites 
To run the app, first make sure you have python3 and pip in your computer:
```
```

Then, create venv and install dependencies as listed from `requirements.txt`:

```
```
# The app
1. `cd` to this root directory and run pip install

```
fastapi dev main.py
```

2. The api is all written inside `controllers` folder, 
   the core logic (with Composite Pattern and Template Method) is in `compute_tax.py` , 
   database setup is in `db.py` ,
   and database & API validation models are in `models` folder,
   the API is setup at `main.py`
3. With FastAPI, The data validation happens automatically with pydantic class
4. Similar to other backend frameworks, FastAPI uses dependency injections thru various decorators to add middlewares, such as DB Session. 


