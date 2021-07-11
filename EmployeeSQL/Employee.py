import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from password import postgrespwd

engine = create_engine(f'postgresql://postgres:{postgrespwd}@localhost:5432/employee_db')
connection = engine.connect()

avg_salary = pd.read_sql('select title as "Employee Title" , round(avg(salary),2) as "Average Salary" from employees e join salaries s on s.emp_no = e.emp_no join titles t on e.emp_title_id = t.title_id group by title', connection)
print(avg_salary)

salary = pd.read_sql('select salary as "Employee Salary", e.emp_no as "Employee Num"\
                     from employees e join salaries s on s.emp_no = e.emp_no ', connection)
print(salary)

salary.hist(column='Employee Salary')

plt.bar(avg_salary["Employee Title"], avg_salary["Average Salary"])
plt.title("Average Salary by Title")
plt.xlabel("Title")
plt.ylabel("Avg Salary")
plt.xticks(rotation=80)
plt.show()

# Epilogue
print(pd.read_sql('select * from employees where emp_no = 499942', connection))
