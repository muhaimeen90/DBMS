/*
select student from taken 
where course in (select course from required)
group by student
having count(*)= (select count(*) from required) ;
*/

select student from taken
minus
select student from (
select student, course from (select student from taken),required 
minus
select student,course from taken
);