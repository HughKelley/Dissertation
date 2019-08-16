--combine the results into two tables

-- http://www.postgresqltutorial.com/postgresql-joins/

-- a table of origin destination attributes
-- origin_lsoa, dest_lsoa, origin_osmid, dest_osmid, origin_centroid, dest_centroid, origin_node_point, dest_node_point, quant distance, centroid distance, node distance. 


-- a table of distances for teh various networks by pair


select * from quant_subset limit 1;

create temp table if not exists first_agg as (select origin as quant_origin_code, destination as quant_dest_code, crow_flies_dist as quant_straight_distance from quant_subset);


select * from nearest_node limit 1;

select lsoa11cd, centroid, nearest_common_node, node_geom from nearest_node;

-- left join structure
SELECT
    a.id id_a,
    a.fruit fruit_a,
    b.id id_b,
    b.fruit fruit_b
FROM
    basket_a a
LEFT JOIN basket_b b ON a.fruit = b.fruit;
----------------------------------


-- add origin data
create temp table if not exists 
	second_agg as (
select 
	a.quant_origin_code quant_origin_code, 
	a.quant_dest_code quant_dest_code,
	a.quant_straight_distance quant_straight_dist,
	b.centroid origin_centroid,
	b.nearest_common_node origin_node_id,
	b.node_geom origin_node_geom
from
	first_agg a 
left join 
	nearest_node b
on 
	a.quant_origin_code = b.lsoa11cd
);


select * from second_agg limit 1;

-- add destination data 

create temp table if not exists 
	third_agg as (
select 
	a.quant_origin_code quant_origin_code, 
	a.quant_dest_code quant_dest_code,
	a.quant_straight_dist quant_straight_dist,
	a.origin_centroid origin_centroid,
	a.origin_node_id origin_node_id,
	a.origin_node_geom origin_node_geom,
	b.centroid dest_centroid,
	b.nearest_common_node dest_node_id,
	b.node_geom dest_node_geom
from
	second_agg a 
left join 
	nearest_node b
on 
	a.quant_dest_code = b.lsoa11cd
);

-------------------------------------------------------------------------------

select * from third_agg limit 1;

------------------------------------------------------------------------------

--add column for node distances


create temp table if not exists fourth_agg as (
select 
	*, 
	st_distance(origin_node_geom, dest_node_geom) as node_dist 
from third_agg
);

select * from fourth_agg limit 10;

-- add column for centroid distances

create temp table if not exists fifth_agg as (
select 
	*, 
	st_distance(origin_centroid, dest_centroid) as centroid_dist 
from fourth_agg
);

select * from fifth_agg limit 10;


-- make table permanent. 


create table if not exists o_d_points_aggregate as (
	select * from fifth_agg
);

select * from o_d_points_aggregate limit 10;

--------------------------------------------------------------------------------------------------------------------------------------------------


-- add missing calcs to undirected_travel_times_1

select * from missing_calcs limit 1;
--index, origin, dest, distance

select * from undirected_travel_times_1 limit 1;
--pidd, net_filter, origin, destination, has_path, distance

select distinct has_path from undirected_travel_times_1;


select count(*) from missing_calcs;
--114,176

select count(*) from undirected_travel_times_1;
--684,166

--sum = 798,342

select count(*) from undirected_travel_times_2;
-- 797,450

-- full matrix size
-- 894 * 894 = 799,236

-- unidrected_travel_times_2
-- 799,236 - 797,450 = 1786
select 799236 - 797450;

select 1786 /2;
-- 893
--one lsoa got missed?

-- 
-- 799,236 - 798,342 = 894
select 799236 - 798342;

-- check duplicate values
select 
a.origin
from undirected_travel_times_1 a 
inner join missing_calcs b on a.origin = b.origin and a.destination = b.dest;
--returns 0 rows, no overlap. 

create temp table if not exists first_u_travel_1_all as ( select origin, destination dest, distance from undirected_travel_times_1 union select origin, dest, distance from missing_calcs);


create temp table if not exists second_u_travel_1_all as (select *, true as has_path from first_u_travel_1_all);

select count(*) from second_u_travel_1_all;
select * from second_u_travel_1_all limit 1;

create temp table if not exists third_u_travel_1_all as (select *, 1 as net_filter from second_u_travel_1_all);

select * from third_u_travel_1_all limit 1;
select count(*) from third_u_travel_1_all;

-- make it permanent

create table if not exists all_undirected_travel_times_1 as (select * from third_u_travel_1_all);

------------------------------------------------------------------------------------------------------------------------------

select * from o_d_points_aggregate limit 1;
select count(*) from o_d_points_aggregate;
-- 799,236

create table if not exists path_dist_agg as (select quant_origin_code, quant_dest_code, origin_node_id, dest_node_id from o_d_points_aggregate);


------------------------------------
------------------------------------
-- o_d_points_aggregate
-- aggs the geometries of the origin and destination centroids and nodes
------------------------------------
-- path_dist_agg 
-- aggs the calculated distances for each pair for each network. 
------------------------------------
------------------------------------

-- join distances into path_dist_agg. 

select * from path_dist_agg limit 1;

select * from all_undirected_travel_times_1 limit 1;

select * from undirected_travel_times_2 limit 1;

select * from travel_times_1 limit 1;

select * from travel_times_2 limit 1;

select count(*) from travel_times_1;
-- 797,450
select count(*) from travel_times_2;
--797,450
select count(*) from undirected_travel_times_2;
-- 797,450
select count(*) from all_undirected_travel_times_1;
-- 798,342
select count(*) from path_dist_agg;
--799,236


---------------------------------------------------------------------------------------------------------------------------------------------------
create temp table if not exists agg_dist_1 as (
select 
	a.quant_origin_code quant_origin_code,
	a.quant_dest_code quant_dest_code,
	a.origin_node_id origin_node_id,
	a.dest_node_id dest_node_id,
	b.distance undirected_1_distance
from 
	path_dist_agg a
left join 
	all_undirected_travel_times_1 b
on a.origin_node_id = b.origin and a.dest_node_id = b.dest
);
-- 799,236
select count(undirected_1_distance) from agg_dist_1;
-- 798,342
select * from agg_dist_1 limit 10;

--alter table agg_dist_1 rename column directed_1_distance to undirected_1_distance;
---------------------------------------------------------------------------------------------------------------------------------------------------

create temp table if not exists agg_dist_2 as ( 
select 
	a.quant_origin_code quant_origin_code,
	a.quant_dest_code quant_dest_code,
	a.origin_node_id origin_node_id,
	a.dest_node_id dest_node_id,
	a.undirected_1_distance undirected_1_distance,
	b.distance directed_1_distance
from 
	agg_dist_1 a 
left join 
	travel_times_1 b 
on a.origin_node_id = b.origin and a.dest_node_id = b.destination
);
-- 799,236
select count(directed_1_distance) from agg_dist_2;
-- 796, 558

select * from agg_dist_2 limit 10;
---------------------------------------------------------------------------------------------------------------------------------------------------

select * from travel_times_2 limit 1;
select count(*) from travel_times_2 where has_path = true;
-- 464,359

create temp table if not exists agg_dist_3 as( 
select
	a.quant_origin_code quant_origin_code,
	a.quant_dest_code quant_dest_code,
	a.origin_node_id origin_node_id,
	a.dest_node_id dest_node_id,
	a.undirected_1_distance undirected_1_distance,
	a.directed_1_distance directed_1_distance,
	b.distance directed_2_distance
from 
	agg_dist_2 a
left join 
	travel_times_2 b
on 
	a.origin_node_id = b.origin and a.dest_node_id = b.destination
);
-- 799,236

select count(directed_2_distance) from agg_dist_3;
-- 464,359

select * from agg_dist_3 limit 10;

---------------------------------------------------------------------------------------------------------------------------------------------------

select * from undirected_travel_times_2 limit 1;
select count(*) from undirected_travel_times_2 where has_path = true;
--502,746

create temp table if not exists agg_dist_4 as ( 
select 
	a.quant_origin_code quant_origin_code,
	a.quant_dest_code quant_dest_code,
	a.origin_node_id origin_node_id,
	a.dest_node_id dest_node_id,
	a.undirected_1_distance undirected_1_distance,
	a.directed_1_distance directed_1_distance,
	a.directed_2_distance directed_2_distance,
	b.distance undirected_2_distance
from 
	agg_dist_3 a
left join 
	undirected_travel_times_2 b
on 
	a.origin_node_id = b.origin and a.dest_node_id = b.destination
);
-- 799,236

select count(undirected_2_distance) from agg_dist_4;
-- 502,746

select * from agg_dist_4 limit 10;


-----------------------------------------------------------------------------------------------------------------------------------------------------

-- persist

create table if not exists distances_1 as (select * from agg_dist_4);

select * from distances_1 limit 100;

---------------------------------------------------------------------------------------------------------------------------------------------------

-- check completeness of data

select count(*) from distances_1 where quant_origin_code = quant_dest_code
-- 894

select distinct directed_1_distance from distances_1 where quant_origin_code = quant_dest_code;

select count(*) from distances_1 where quant_origin_code != quant_dest_code and directed_2_distance is null;
-- 1: 1,784
-- 2: 333,983
-- u_2: 295,596
-- u_1: 0

select count(*) from travel_times_2 where has_path is false;
-- 1: 892
-- 2: 333,091
-- u_2: 294,704
-- u_1: 0

--differences
-- 1: 892
-- 2:892
-- u_2: 892
-- u_1: 0


--SELECT
--    a.id id_a,
--    a.fruit fruit_a,
--    b.id id_b,
--    b.fruit fruit_b
--FROM
--    basket_a a
--LEFT JOIN basket_b b ON a.fruit = b.fruit;
-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
-- directed network 1

-- get missing values from agg table into individual tables

select * from distances_1 limit 1;
select count(*) from distances_1;
-- 799,236
select count(*) from distances_1 where origin_node_id = dest_node_id;
-- 894



create temp table if not exists first_missing_d_1 as (  
select * from distances_1 where quant_origin_code != quant_dest_code and directed_1_distance is null
);	



create temp table if not exists no_path_d_1 as (
select * from travel_times_1 where has_path = false 
);

select * from no_path_d_1;
-- origin 5,816,785,884
select count(*) from no_path_d_1;
select count(*) from first_missing_d_1;
select * from no_path_d_1 limit 1;
select * from first_missing_d_1 limit 1;

create temp table if not exists second_missing_d_1 as ( 
select
a.origin_node_id origin_node_id,
a.dest_node_id dest_node_id,
b.pid pid
from 
	first_missing_d_1 a
left join 
	no_path_d_1 b
on a.origin_node_id = b.origin and a.dest_node_id = b.destination
where b.pid is null
);
-- 892
select * from second_missing_d_1;
	
create table if not exists missing_d_1 as ( select * from second_missing_d_1)

select * from missing_d_1;

-- run python script

select * from missing_calc_d_1;

------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------
-- directed network 2 

select * from distances_1 limit 1;
select count(*) from distances_1;
-- 799,236
select count(*) from distances_1 where origin_node_id = dest_node_id;
-- 894



create temp table if not exists first_missing_d_2 as (  
select * from distances_1 where quant_origin_code != quant_dest_code and directed_2_distance is null
);
-- 333,983


create temp table if not exists no_path_d_2 as (
select * from travel_times_2 where has_path = false 
);
-- 333,091

select * from no_path_d_2 limit 1;

create temp table if not exists second_missing_d_2 as ( 
select
a.origin_node_id origin_node_id,
a.dest_node_id dest_node_id,
b.pidd pidd
from 
	first_missing_d_2 a
left join 
	no_path_d_2 b
on a.origin_node_id = b.origin and a.dest_node_id = b.destination
where b.pidd is null
);
-- 892

select * from second_missing_d_2;
select count(distinct dest_node_id) from second_missing_d_2;
-- it's like their randomly missing. 
-- Something about commiting to the database??

create table if not exists missing_d_2 as ( select * from second_missing_d_2);

select * from missing_calc_d_2;

------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------
-- undirected network 2 

select * from distances_1 limit 1;

create temp table if not exists first_missing_u_2 as (  
select * from distances_1 where quant_origin_code != quant_dest_code and undirected_2_distance is null
);
-- 295,596

create temp table if not exists no_path_u_2 as (
select * from undirected_travel_times_2 where has_path = false 
);
-- 294,704

select * from no_path_u_2 limit 1;

create temp table if not exists second_missing_u_2 as ( 
select
a.origin_node_id origin_node_id,
a.dest_node_id dest_node_id,
b.pidddd pidddd
from 
	first_missing_u_2 a
left join 
	no_path_u_2 b
on a.origin_node_id = b.origin and a.dest_node_id = b.destination
where b.pidddd is null
);
-- 892

select count(distinct origin_node_id) from second_missing_u_2;

create table if not exists missing_u_2 as ( select * from second_missing_u_2);
-- 892


------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------

--union missing values into old tables

select * from travel_times_1 limit 1;
-- pid, net_filter, origin, destination, has_path, distance

select * from missing_calc_d_1 limit 1;
-- index, origin, dest, distance

-- change column names where necessary

-- add columns where necessary

create temp table if not exists third_u_travel_1_all as (select *, 1 as net_filter from second_u_travel_1_all);

create temp table if not exists second_u_travel_1_all as (select *, true as has_path from first_u_travel_1_all);

-- union

create temp table if not exists first_u_travel_1_all as ( select origin, destination dest, distance from undirected_travel_times_1 union select origin, dest, distance from missing_calcs);







