--------------
-- for QUANT data


-- relevant table is quant_subset

select * from quant_subset limit 1;
-- not clear why I included the lad11cd columns. 
-- origin, destination, crow, and time looked consistent when I checked. 

select * from quant limit 1;
--6.658527, 29.8989400228

select * from quant where origin = 'E01000848' and destination = 'E01001959';

select count(*) from quant_subset;
--799,236

select count(*) from quant_subset where travel_time_mins = 0 and crow_flies_dist != 0;
-- 200,0,41
-- missing non-loop values

select count(*) from quant_subset where travel_time_mins = 0 and crow_flies_dist = 0;
-- 894 loop values. 



-- replace 0's with null

select count(case when (crow_flies_dist != 0 and travel_time_mins = 0) then null else travel_time_mins end)  from quant_subset;

---------------------------------------------------------------------------------------
select * from quant_subset limit 1;
select count(*) from quant_subset;
select count(*) from quant_subset where origin = destination;

create temp table if not exists temp_clean_quant as (select origin, destination, crow_flies_dist, nullif(travel_time_mins, 0) from quant_subset where crow_flies_dist != 0);
-- 798,342

create table if not exists clean_quant_subset as (select * from temp_clean_quant);
-- 798,342

--select case when (parent is null and flag01 = 'OK' and flag02 = 'OK') 
--       then 'CT_00000'
--       else parent end as columnSomeName,
--       Child, flag01, lag02
-- from yourTable;