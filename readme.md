# Introduction
I've written the solutions in Python language with FASTAPI framework.
Python have classes and allow inheritances for OOP , but not implementations and interface (unlike java).
For the OOP Design Pattern, I've done `Template Method pattern` as well as `Composite pattern`, 
For further details on Design Pattern, I've attached UML diagrams to list all my implementations.
I've written the API with FASTAPI framework.

# Database (DB)
Database (often shortened to DB in my comments) is using `sqlite`.
`This is for simplicity for testing the app.`
In real world commercial scale, I would recommend using PostgreSQL or MongoDB or other enterprise grade DB, depending on the use case. 
Once the app starts, the DB will create a `employee_salaries.db` file at the root of this app directory. 

# Pre-requisites 
To run the app, first make sure you have python3 and pip in your computer, here is the version i used:
```
(venv) backend-test-advance % python3 --version  
Python 3.9.6
(venv) backend-test-advance % pip --version
pip 21.2.4 from /backend-test-advance/venv/lib/python3.9/site-packages/pip (python 3.9)
```

Then, create venv :

```
python -m venv venv
venv\Scripts\activate # bash
.\venv\Scripts\activate # PowerShell
source venv/bin/activate # macOS or Linux or Git Bash
```
Once venv activated it will look like this:
```
(venv) $
```


`ALWAYS MAKE SURE YOU ARE USING VENV (i.e. venv is activated) before doing anything else!`

# The app
`AFTER successful activation of your venv as stated above`, `cd` to this app's root directory, and then `run pip install from requirements.txt`:
```
pip install -r requirements.txt
```

Then run the app:
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

# Server
```
Server starts at http://127.0.0.1:8000
Server Documentation at http://127.0.0.1:8000/docs  
```
Documentation is using Swagger UI. FASTAPI autogenerates this by default.
You can test the API through the Swagger UI at `http://127.0.0.1:8000/docs`


# APIs
There's 3 APIs written:

- `/` returns Hello World
- GET `/employee_salaries` to get all salaries stored in database.
    - it runs SELECT query statement in the ORM, so you can give offset and limit the query (`NOTE: default limit is 100 items output into the JSON`)
    
- POST `/employee_salaries` with employee name and annual salary amount to store into database.
    - POST expects `non empty string for employee name`, and a `string/float annual salary amount`
    - anything other than that is automatically rejected by pydantic. For more examples on what is rejected, you can see `test_main.py` on my unit testing.
    - Float Value is not formatted into 2 decimal places in the DB storage, but for readability purposes, I return them as 2 decimal places in POST request only.

# Testing
1. all tests are written in `test_main.py`
2. Run these to install:
```
pip install pytest
```

3. To test,`cd` to this app's root directory, and run :
```
pytest

EXPECTED OUTPUT:
======================= 6 passed, 2 warnings in X.XXs =========================================================================================
```

# Tax Calculation
Tax calculation is using `Composite` and `Template Method` Design Pattern for decoupling purposes. 
This is explained in the `OOP UML Class Diagram.pdf` diagram that I've submitted.
`Please note` that in my implementation, I use 2 decimal places since it's a currency, and I mostly use `float` data type to deal with numbers.
Also, `please note` that `compute_tax_simple.py` is my prototype proofing before adding `design patterns` in, so  you can safely ignore that file. 

The implementation classes with design pattern is located at `compute_tax.py` 
it has `__main__` execution block, so you can run it by simply calling:
```
python3 compute_tax.py
```
I've already used the same tests as written in the instructions.

they will output like this:
```
(venv) gvincenta@Gilberts-MacBook-Pro backend-test-advance % python3 compute_tax.py

Name: Gilbert | Annual Salary 60,000.20

+-------------------------+----------+---------------+---------------+
|Salary Bracket           |   Rate   | Taxable Amount|      Total Tax|
+-------------------------+----------+---------------+---------------+
|first 0 - 20000          |  0.00   %|      20,000.00|           0.00|
|next 20001-40000         |  10.00  %|      20,000.00|       2,000.00|
|next 40001-80000         |  20.00  %|      20,000.20|       4,000.04|
|next 80001-180000        |  30.00  %|           0.00|           0.00|
|180001 and above         |  40.00  %|           0.00|           0.00|
+-------------------------+----------+---------------+---------------+
|**Total**                |          |      60,000.20|       6,000.04|
+-------------------------+----------+---------------+---------------+

Name: Maymay | Annual Salary 80,150.15

+-------------------------+----------+---------------+---------------+
|Salary Bracket           |   Rate   | Taxable Amount|      Total Tax|
+-------------------------+----------+---------------+---------------+
|first 0 - 20000          |  0.00   %|      20,000.00|           0.00|
|next 20001-40000         |  10.00  %|      20,000.00|       2,000.00|
|next 40001-80000         |  20.00  %|      40,000.00|       8,000.00|
|next 80001-180000        |  30.00  %|         150.15|          45.04|
|180001 and above         |  40.00  %|           0.00|           0.00|
+-------------------------+----------+---------------+---------------+
|**Total**                |          |      80,150.15|      10,045.04|
+-------------------------+----------+---------------+---------------+

Name: Anton | Annual Salary 200,000.80

+-------------------------+----------+---------------+---------------+
|Salary Bracket           |   Rate   | Taxable Amount|      Total Tax|
+-------------------------+----------+---------------+---------------+
|first 0 - 20000          |  0.00   %|      20,000.00|           0.00|
|next 20001-40000         |  10.00  %|      20,000.00|       2,000.00|
|next 40001-80000         |  20.00  %|      40,000.00|       8,000.00|
|next 80001-180000        |  30.00  %|     100,000.00|      30,000.00|
|180001 and above         |  40.00  %|      20,000.80|       8,000.32|
+-------------------------+----------+---------------+---------------+
|**Total**                |          |     200,000.80|      48,000.32|
+-------------------------+----------+---------------+---------------+

Name: Ronald | Annual Salary -5.00

+-------------------------+----------+---------------+---------------+
|Salary Bracket           |   Rate   | Taxable Amount|      Total Tax|
+-------------------------+----------+---------------+---------------+
|first 0 - 20000          |  0.00   %|           0.00|           0.00|
|next 20001-40000         |  10.00  %|           0.00|           0.00|
|next 40001-80000         |  20.00  %|           0.00|           0.00|
|next 80001-180000        |  30.00  %|           0.00|           0.00|
|180001 and above         |  40.00  %|           0.00|           0.00|
+-------------------------+----------+---------------+---------------+
|**Total**                |          |          -5.00|           0.00|
+-------------------------+----------+---------------+---------------+
```