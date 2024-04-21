Create or Replace Function taxed_sal 
(p_id employees.employee_id%type) Return Number IS
v_sal employees.salary%type := 0;

Begin
Select ((salary+salary*nvl(commission_pct,0))*12)
Into v_sal
from employees
where employee_id = p_id;
Return v_sal * .08;
End taxed_sal;
/
