Create or replace Procedure Raise_salary(p_id in employees.employee_id%type, p_percent in Number)
is
Begin
Update employees
set salary= salary*(1+p_percent/100)
Where employee_id=p_id;
End Raise_salary;
/

create or replace procedure query_emp
(p_id IN employees.employee_id%type,
p_name OUT employees.last_name%type,
p_salary OUT employees.salary%type) is
Begin
select last_name, salary into p_name, p_salary from employees
where employee_id= p_id;
End query_emp;
/

DECLARE
v_emp_name employees.last_name%type;
v_emp_sal employees.salary%type;
BEGIN
query_emp(171,v_emp_name, v_emp_sal);
DBMS_OUTPUT.PUT_LINE (v_emp_name || ' earns ' || to_char(v_emp_sal, '$999,999.00'));
END;
/