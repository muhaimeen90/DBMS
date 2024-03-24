create or replace procedure format_phone(p_phone_no in out employees.phone_number%type)
IS
BEGIN
p_phone_no:= '('|| Substr(p_phone_no,1,3)||
		')' || Substr(p_phone_no,4,3)||
		'-' || substr(p_phone_no,7);
end format_phone;
/

declare
v_no employees.phone_number%type;
Begin
v_no :='01815890998';
format_phone(v_no);
DBMS_OUTPUT.PUT_LINE(v_no);
End;
/