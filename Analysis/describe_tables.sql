

select count(*) from london_bike_relation limit 1;


select count(*) from quant;
select count(*) from quant_subset;
select count(*) from quant_subset_missing_links;
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------


select count(*) from relation;
-- 0

select count(*) from relation_edges;
-- 3,222

----------------------------------------
--distance calculation results 

select count(*) from travel_times_1;
-- 797,450
select count(*) from travel_times_2;
-- 797,450
select count(*) from undirected_travel_times_1;
-- 684, 166
select count(*) from undirected_travel_times_2;
-- 797,450

select count(*) from quant_subset;
-- 799,236
-- sqrt(799,236) = 894
-- 799,236 - 797,450 = 1786
-- 1786 / 2 = 893. 
-- because each trip was calculated in 2 directions. 
-- but each self loop only gets skipped once. 



----------------------------------------------------------------





