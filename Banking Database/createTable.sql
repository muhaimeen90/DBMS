create table branch (
	branch_name VARCHAR2(20),
	branch_city VARCHAR2(20),
	assets NuMbER,
	CONSTRAINT branch_pk PRIMARY KEY (branch_name)
);

create table customer(
	customer_name varchar2(20),
	customer_city varchar2(20),
	customer_street varchar2(20),
	constraint customer_pk PRIMARY KEY (customer_name)
);
create table account(
	account_number number,
	branch_name varchar2(20),
	balance number,
	constraint account_pk PRIMARY KEY (account_number),
	constraint account_fk foreign key (branch_name) references branch(branch_name)
);
create table loan(
	loan_number number,
	branch_name varchar2(20),
	amount number,
	constraint loan_pk Primary key (loan_number),
	constraint loan_fk foreign key (branch_name) references branch(branch_name)
);
create table depositor(
	customer_name varchar2(20),
	account_number number,
	constraint depositor_customer_fk foreign key(customer_name) references customer(customer_name),
	constraint depositor_account_fk foreign key(account_number) references account(account_number)
);
create table borrower(
	customer_name varchar2(20),
	loan_number number,
	constraint borrower_customer_fk foreign key(customer_name) references customer(customer_name),
	constraint borrower_loan_fk foreign key(loan_number) references loan(loan_number)
);