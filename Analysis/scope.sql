-- stats for the scope of the investigation

select * from north_inner_subset limit 1;
select * from 

select sum("USUALRES") from north_inner_subset;

select sum("USUALRES") from north_inner_subset;
-- 1,494,742


select sum("USUALRES") from lsoa_table;
-- 8,242,757

select 1494742 / 8242757;

select avg("POPDEN") from north_inner_subset;
--159

select avg("POPDEN") from lsoa_table;
95.8. 

select avg("USUALRES") from lsoa_table;




select * from casualties limit 1;

select count(*) from casualties;
-- 291, 043

select distinct "Borough" from casualties;

select count(*) from casualties where "Borough" in ('CAMDEN', 'HACKNEY', 'HAMMERSMITH & FULHAM', 'ISLINGTON', 'KENSINGTON & CHELSEA', 'TOWER HAMLETS', 'WESTMINSTER', 'CITY OF LONDON');

73,124

select 73124/291043;


