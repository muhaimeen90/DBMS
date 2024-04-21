Declare
v_num1 Number := 3;
v_num2 Number := 4;
v_num3 Number := 5;
v_max Number;
Begin
If v_num1 > v_num2
Then
	If v_num1> v_num3
	Then 
		v_max := v_num1;
	End if;
	If v_num3> v_num1
	Then
		v_max := v_num3;
	End if;
	
End if;
If v_num2> v_num1
Then 
	If v_num2> v_num3
	Then 
		v_max := v_num2;
	End if;
	If v_num3> v_num2
	Then
		v_max := v_num3;
	End if;
End if;
dbms_output.Put_line(v_max);
End;
/





Declare

a varchar2(5) := '&sa';
Begin
If a >= '0' and a <= '9'
Then 
	dbms_output.Put_line('Its a number');
Elsif a >='A' and a <= 'Z'
Then 
	dbms_output.Put_line('Its a capital letter');
Elsif a >= 'a' and a <= 'z'
Then
	dbms_output.Put_line('Its a small letter'); 
Else 
	dbms_output.Put_line('Its a special character');
End if;
End;
/