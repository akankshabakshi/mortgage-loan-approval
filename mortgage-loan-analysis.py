select * from train_labels as tl 
inner join train_values as tv 
on tl.row_id = tv.row_id
where tl.accepted = '1';
----rows * columns of the table train_labels
select count(*) from train_labels;

total records in table: train_labels - 500000
---total rows of row_id field
select count(distinct row_id) from train_labels;
----which concludes that this can be used as a primary field in this table

---Exploring other relevant fields for analysis 
select distinct applicant_race from train_values
---- 1,2,3,4,5,6,7
---let's get back to the audience who's loan got approved
select * from train_values as tv
inner join train_labels as tl
on tv.row_id = tl.row_id limit 5;

---analysis at population level 
select max(population) as max_population from train_values where population 
<(select max(population) from train_values);
---9999 is the highest population 
select min(population) as min_population from train_values
----and 1000 is the lowest population 

----let's try and understand how these majority population  field is related to other fields 
select max(population) as max_population, * from train_values where population 
<(select max(population) from train_values);
---so the values are: 
---loan_amount - 75.0
---row_id - 
---co-applicant: true
---ffexmedian_family_income: 63077 which is greater than the loan amount 
---applicant_sex: 1
---applicant_5: 5

-----population with applicant sex - loan amount
select avg(loan_amount) as loan_amount, applicant_sex from train_values
group by applicant_sex
order by loan_amount desc 

----applicant_sex whose loan got approved
select tv.applicant_sex, tl.accepted from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id

---which highest applicant_sex whose loan got approved
select tv.applicant_sex, count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where accepted = '1'
group by tv.applicant_sex
order by accepted_count desc
---which concludes applicant_sex 1 has highest accepted count for loans 

---to verify we created a separate set to analyse 4 applicant_sex
select tv.applicant_sex, tl.accepted from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where applicant_sex = '1' and accepted = '1'
---total count - 250114
---accepted count = 164479
----which is 52.08%

----which highest property_type whose loan got approved
select tv.property_type, count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where accepted = '1'
group by tv.property_type
order by accepted_count desc
---which concludes property_type 1 is the highest type property whose loan got approved
---Stating the obvious above
---which pre-approval type loan got approved
select tv.preapproval, count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where accepted = '1'
group by tv.preapproval
order by accepted_count desc
---which concludes in case of loan getting approved the preapproval 3 has the highest count 

----can one county code have multiple state codes
select county_code, group_concat(distinct state_code), count(distinct state_code) from train_values
group by county_code
---yes there can multiple state codes for a single county_code

---let's check the opposite
select state_code, group_concat(distinct county_code), count(distinct county_code) from train_values
group by state_code
----yes, there is a many to many mapping between state code and county code 

-----which state codes have highest accepted loans 
select tv.state_code, count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where accepted = '1'
group by tv.state_code
order by accepted_count desc

---what are the chances of loan getting approved if the co-applicant is involved
select tv.co_applicant , count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
group by tv.co_applicant
order by accepted_count desc
---There is relation of co-applicant being involved that can increase the chances of loan getting approved

----what should be the applicant income in order to get the loan approved 
select tv.applicant_income, count(tl.accepted) as accepted_count from train_values tv
inner join train_labels tl
on tv.row_id = tl.row_id
where accepted = '1'
group by tv.applicant_income
order by accepted_count desc
---No relation 

-----Analysis Outcome 
-----1. Applicant_sex '1' has highest accepted count of loans
-----2. Property Type '1' has highest accepted count of loans 
-----3. For loan getting approved, the highest count of preapproval is that of '3'
-----4. State code '37' has the highest count of accepted loans



