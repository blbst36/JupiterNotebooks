-- 1. List the following details of each employee: employee number, last name, first name, sex, and salary.
select e.emp_no as "Employee No", last_name as "Employee Last Name", first_name as "Employee First Name", sex as "Employee Sex", salary as "Employee Salary" 
from employees e
join salaries s on s.emp_no = e.emp_no

-- 2. List first name, last name, and hire date for employees who were hired in 1986.
select first_name as "Employee First Name", last_name as "Employee Last Name", hire_date as "Employee Hire Date"
from employees
where EXTRACT(year FROM hire_date) = 1986

-- 3. List the manager of each department with the following information: department number, department name, the manager's employee number, last name, first name.
select d.dept_no as "Department No", d.dept_name as "Department Name", m.emp_no as "Manager No", e.last_name as "Manager Last Name", e.first_name as "Manager First Name"
from departments d
join dept_manager m on m.dept_no = d.dept_no 
join employees e on e.emp_no = m.emp_no

-- 4. List the department of each employee with the following information: employee number, last name, first name, and department name.
select e.emp_no as "Employee No", last_name as "Employee Last Name", first_name as "Employee First Name", dep.dept_name as "Department Name"
from employees e
join dept_emp d on e.emp_no = d.emp_no
join departments dep on dep.dept_no = d.dept_no

-- 5. List first name, last name, and sex for employees whose first name is "Hercules" and last names begin with "B."
select first_name as "Employee First Name", last_name as "Employee Last Name", sex as "Employee Sex"
from employees
where first_name = 'Hercules' and last_name like 'B%'

-- 6. List all employees in the Sales department, including their employee number, last name, first name, and department name.
select e.emp_no as "Employee No", last_name as "Employee Last Name", first_name as "Employee First Name", dep.dept_name as "Department Name"
from employees e
join dept_emp d on e.emp_no = d.emp_no
join departments dep on dep.dept_no = d.dept_no
where dep.dept_name = 'Sales'

-- 7. List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
select e.emp_no as "Employee No", last_name as "Employee Last Name", first_name as "Employee First Name", dep.dept_name as "Department Name"
from employees e
join dept_emp d on e.emp_no = d.emp_no
join departments dep on dep.dept_no = d.dept_no
where dep.dept_name in ('Sales', 'Development')

-- 8. In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
select last_name as "Employee Last Name", count(emp_no) as "Name Count"
from employees
group by last_name
order by "Name Count" desc
