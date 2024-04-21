Create or Replace Function get_sal 
(p_id employees.employee_id%type) Return Number IS
v_sal employees.salary%type := 0;
Begin
Select salary
Into v_sal
from employees
where employee_id = p_id;
Return v_sal;
End get_sal;
/


select get_sal(employee_id) from employees;


DECLARE
v_emp_sal employees.salary%type;
BEGIN
v_emp_sal := get_sal(100);
DBMS_OUTPUT.PUT_LINE (v_emp_sal);
END;
/


Execute dbms_output.put_line(get_sal(100));