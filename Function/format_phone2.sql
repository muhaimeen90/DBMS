create table phone_number (
	p_id number,
	p_no varchar2(20)
);
create table phone_number2(
	p_no varchar2(20)
);

insert into phone_number values(1,'01815890998');
insert into phone_number values(2,'01815890991');
insert into phone_number values(3,'01815890993');

create or replace procedure format_phone(p_phone_no in out phone_number.p_no%type)
IS
BEGIN
p_phone_no:= '('|| Substr(p_phone_no,1,3)||
		')' || Substr(p_phone_no,4,3)||
		'-' || substr(p_phone_no,7);
end format_phone;
/

create or replace procedure query_no
(p1_id IN phone_number.p_id%type,
p1_no out phone_number.p_no%type) is
Begin
select p_no into p1_no from phone_number
where p1_id= p_id;
End query_no;
/
declare
v_no phone_number.p_no%type;
Begin
query_no(1,v_no);
format_phone(v_no);
Insert into phone_number2 values(v_no);
query_no(2,v_no);
format_phone(v_no);
Insert into phone_number2 values(v_no);
query_no(3,v_no);
format_phone(v_no);
Insert into phone_number2 values(v_no);
End;
/
select * from phone_number2;
