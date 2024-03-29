select distinct Depositor.customer_name
from depositor,account 
where depositor.account_number=account.account_number and branch_name 
in(select branch_name from branch where branch_city='Dhaka') 
group by customer_name 
having count(*)=(select count(branch_name) from branch where branch_city='Dhaka');
