select distinct student from taken
 where course in(select course from required);