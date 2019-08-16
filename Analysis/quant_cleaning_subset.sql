-- getting QUANT data ready for shortest path calculation

select * from quant limit 1;

select count(*) from quant;
-- 23,377,225

--subset by lsoa's in north inner subset

select * from north_inner_subset limit 1;

-- LSOA11CD is E01004295
-- LAD11CD is E09000030

select * from lsoa_table where "LSOA11CD" = 'E01000001';
-- has a result, so that's the field that the QUANT data is using to identify



--a left join 
--SELECT
--    a.id id_a,
--    a.fruit fruit_a,
--    b.id id_b,
--    b.fruit fruit_b
--FROM
--    basket_a a
--LEFT JOIN basket_b b ON a.fruit = b.fruit;

create temp table if not exists quant_origin_subset as (
select 
	a."LAD11CD" lad11cd_a,
	b.origin,
	b.destination,
	b.crow_flies_dist,
	b.travel_time_mins
from 
	north_inner_subset a 
left join quant b on a."LSOA11CD" = b.origin
);

select * from quant_origin_subset limit 1;

create temp table if not exists quant_both_subset as (
select 
	a."LAD11CD" lad11cd_a,
	b.lad11cd_a lad11cd_a_b,
	b.origin,
	b.destination,
	b.crow_flies_dist,
	b.travel_time_mins
from 
	north_inner_subset a 
left join quant_origin_subset b on a."LSOA11CD" = b.destination
);

select * from quant_both_subset limit 1;

select count(*) from quant_both_subset;
-- 799,236

create table if not exists quant_subset as (select * from quant_both_subset);

select * from quant_subset limit 1;

select count(*) from quant_subset where crow_flies_dist != 0 and travel_time_mins = 0;
-- 200,041

--save as a table

--drop table quant_subset_missing_links;
create table if not exists quant_subset_missing_links as (select * from quant_subset where crow_flies_dist != 0 and travel_time_mins = 0);

----------------------------------------------------------------------------------------------------
-- convert crow flies distance to travel time

-- 
select count(*) from quant_subset limit 1;
select count(*) from clean_quant_subset limit 1;
select * from clean_quant_subset limit 1;

alter table clean_quant_subset rename column "nullif" to travel_time_mins;

drop table clean_quant_subset_times;

create table if not exists clean_quant_subset_times as (
select origin, destination, travel_time_mins, (crow_flies_dist / 4.83 * 60) as walking_time_mins from clean_quant_subset
) ;

select * from clean_quant_subset_times limit 1;




---------------------------------------------------------------------------------------------

select count(*) from clean_quant_subset limit 1;
-- 798,342
select * from clean_quant_subset limit 1;

select count(travel_time_mins) from clean_quant_subset;
-- 598,301




