create table employees(
emp_no int primary key,
emp_title_id varchar(10) NOT NULL,
birth_date date,
first_name varchar(30),
last_name varchar(30),
sex varchar(1),
hire_date date);

create table departments(
dept_no varchar(10) primary key,
dept_name varchar(30));

create table titles(
title_id varchar(10) primary key,
title varchar(30));

create table salaries(
emp_no int,
salary int,
primary key(emp_no, salary),
foreign key (emp_no) references employees(emp_no));

create table dept_manager(
dept_no varchar(10),
emp_no int,
primary key (dept_no, emp_no),
foreign key (emp_no) references employees(emp_no),
foreign key (dept_no) references departments(dept_no));

create table dept_emp(
emp_no int,
dept_no varchar(10),
primary key (emp_no, dept_no),
foreign key (emp_no) references employees(emp_no),
foreign key (dept_no) references departments(dept_no));
