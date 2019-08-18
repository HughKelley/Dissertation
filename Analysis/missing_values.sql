-- get table of od pairs that are not in undirected 1 travel times


-- remove pairs where origin = destination. 

select * from undirected_travel_times_1 limit 1;
select * from o_d_points_aggregate limit 1;

select count(*) from undirected_travel_times_1;
select count(*) from travel_times_1;
-- 797,450 - 684,166 = 113,284 missing pairs

create temp table if not exists first_missing_pairs as (
select 
	a.quant_origin_code origin_code,
	a.quant_dest_code dest_code,
	a.origin_node_id origin_node_id,
	a.dest_node_id dest_node_id,
	b.origin
from 
	o_d_points_aggregate a
left join undirected_travel_times_1 b on a.origin_node_id = b.origin and a.dest_node_id = b.destination
where b.origin is null
);

--table with 115,070 rows

--drop loops

select count(*) from first_missing_pairs where origin_code != dest_code;

create temp table if not exists second_missing_pairs as (
	select * from first_missing_pairs where origin_code != dest_code
);

select * from second_missing_pairs limit 1;

create table if not exists missing_pairs as (select * from second_missing_pairs);

select * from missing_pairs limit 1;

select count(*) from missing_pairs where dest_node_id = 106805;
--128


select count(*) from missing_pairs where origin_node_id = 106805;

select count(*) from missing_calcs;	
-- start time 10:30 on the nose. 

--drop table missing_calcs;


--SELECT
--    a.id id_a,
--    a.fruit fruit_a,
--    b.id id_b,
--    b.fruit fruit_b
--FROM
--    basket_a a
--LEFT JOIN basket_b b ON a.fruit = b.fruit
--WHERE b.id IS NULL;