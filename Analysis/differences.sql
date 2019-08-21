-----   prepping data for histograms

select * from o_d_points_aggregate limit 10;

drop table node_centroid_dist_diffs;

create table if not exists node_centroid_dist_diffs as (
	select 
		node_dist - centroid_dist as differences
	from 
		o_d_points_aggregate 
	where
		quant_origin_code != quant_dest_code
);

select * from node_centroid_dist_diffs limit 10;



drop table primary_trunk_net;

select * from o_d_points_aggregate limit 10;

select quant_straight_dist, node_dist from o_d_points_aggregate;


--drop table quant_node_dist_diff;

create temp table if not exists first_quant_node_dist_diff as (select quant_straight_dist * 1000 as quant_dist, node_dist from o_d_points_aggregate where quant_origin_code != quant_dest_code);

select * from first_quant_node_dist_diff limit 10;


create table if not exists quant_node_dist_diff as (select quant_dist - node_dist as difference from first_quant_node_dist_diff);


----------------------------------------------------------------------------------------------------------------------------------------------

-- data for map of d1 - quant

select * from all_agg_times limit 10;

create temp table if not exists first_quant_d_1_time_diff as (
select quant_origin, quant_dest, d_1_time, quant_time from all_agg_times where d_1_time is not null and quant_time is not null
);
-- 597,528

create temp table if not exists second_quant_d_1_time_diff as (
select quant_origin, quant_dest, d_1_time - quant_time as difference from first_quant_d_1_time_diff
);

select * from second_quant_d_1_time_diff limit 10;


create temp table if not exists third_quant_d_1_time_diff as ( 
select quant_origin, avg(difference) as avg_diff from second_quant_d_1_time_diff group by quant_origin
);
-- 773

select * from north_inner_subset limit 10;
select * from third_quant_d_1_time_diff limit 10;

create temp table if not exists 
	fourth_quant_d_1_time_diff 
as (
	select 
		a.quant_origin,
		a.avg_diff,
		b.geom
	from
		third_quant_d_1_time_diff a 
	left join
		north_inner_subset b 
	on 
		a.quant_origin = b."LSOA11CD"
);

select * from fourth_quant_d_1_time_diff;
create table if not exists quant_d_1_time_diff as (select * from fourth_quant_d_1_time_diff);

---------------------------------------------------------------------------------------------------------------
-- d_1_d_2_directness_diff

select * from all_agg_directness limit 10;

create temp table if not exists	
	first_d_1_d_2_direct_diff 
as ( 
	select 
		quant_origin,
		quant_dest,
		d_1_direct,
		d_2_direct
	from 
		all_agg_directness
	where
		d_1_direct is not null 
		and 
		d_2_direct is not null	
);

-- 464,988

select * from first_d_1_d_2_direct_diff limit 100;

--select d_1_direct - d_2_direct as difference from first_d_1_d_2_direct_diff limit 100;
drop table second_d_1_d_2_direct_diff;

create temp table if not exists 
	second_d_1_d_2_direct_diff 
as ( 
	select 
		quant_origin,
		quant_dest,
		d_2_direct - d_1_direct as difference
	from first_d_1_d_2_direct_diff
);

select count(distinct difference) from second_d_1_d_2_direct_diff;
select * from second_d_1_d_2_direct_diff limit 100;


create temp table if not exists  third_d_1_d_2_direct_diff as (
	select 
		quant_origin,
		avg(difference) as avg_diff_direct
	from
		second_d_1_d_2_direct_diff
	group by quant_origin
);

select * from north_inner_subset limit 10;

create temp table if not exists 
	fourth_d_1_d_2_direct_diff 
as (
	select 
		a.quant_origin,
		a.avg_diff_direct,
		b.geom
	from
		third_d_1_d_2_direct_diff a 
	left join
		north_inner_subset b 
	on 
		a.quant_origin = b."LSOA11CD"
);


-- 780
select * from fourth_d_1_d_2_direct_diff limit 100;

create table if not exists 
	d_1_d_2_direct_diff 
as (
	select * from fourth_d_1_d_2_direct_diff
);


---------------------------------------------------------------------------------------------------------------------------------------
-- time difference with quant plus
select * from all_agg_times limit 100;

create temp table if not exists first_quant_plus_d1_time_diff as (select quant_origin, quant_dest, d_1_time, quant_time_plus from all_agg_times where d_1_time is not null and quant_time_plus is not null);
-- 797,49

create temp table if not exists second_quant_plus_d1_time_diff as (select quant_origin, ((d_1_time - quant_time_plus) / quant_time_plus) as perc_diff from first_quant_plus_d1_time_diff);

--drop table third_quant_plus_d1_time_diff;

create temp table if not exists third_quant_plus_d1_time_diff as (select quant_origin, avg(perc_diff) as avg_perc_diff from second_quant_plus_d1_time_diff group by quant_origin);

select * from third_quant_plus_d1_time_diff limit 100;

-- then join geometries in

create temp table if not exists 
	fourth_quant_plus_d1_time_diff 
as (
	select 
		a.quant_origin,
		a.avg_perc_diff,
		b.geom
	from	
		third_quant_plus_d1_time_diff a
	left join
		north_inner_subset b
	on 
		a.quant_origin = b."LSOA11CD"
);


select * from fourth_quant_plus_d1_time_diff limit 100;

select max(avg_perc_diff) from fourth_quant_plus_d1_time_diff ;

create table if not exists quant_plus_d1_time_diff as (select * from fourth_quant_plus_d1_time_diff );

---------------------------------------------------------------------------------------------------------------------------------------------
-- difference in directness across directed and undirected

select * from all_agg_distances limit 10;

drop table d1_d2_dist_diff;

create table if not exists d1_d2_dist_diff as (
select dest_node, origin_node, ((d_2_distance - d_1_distance) / d_1_distance) as perc_diff_dist, d_1_distance from all_agg_distances
);

select count(dest_node) from d1_d2_dist_diff where perc_diff_dist < 0 group by dest_node;

select * from d1_d2_dist_diff limit 100;

select origin_node, dest_node, perc_diff_dist, d_1_distance from d1_d2_dist_diff where perc_diff_dist is not null and d_1_distance > 10000 and perc_diff_dist < 0.1 order by perc_diff_dist desc limit 500;



----------------------------------------------------------------------------------------------------------------------------------------------

select count(*) from agg_times_no_nulls;
select * from agg_times_no_nulls limit 10;
select * from all_agg_directness;
select avg(u_1_time) avg_u1, avg(d_1_time) avg_d1, avg(u_2_time) avg_u2, avg(d_2_time) avg_d2  from agg_times_no_nulls;


-----------------------------------------------------------------------------------------------------------------------------------------------

select * from all_agg_times limit 1;

select count(*) from all_agg_times;
-- 798,342

select count(u_1_time) u1, count(d_1_time) d1, count(u_2_time) u2, count(d_2_time) d2 from all_agg_times;






---------------------------------------------------------------------------------------------------------------------------------------------

select * from all_quant_times limit 1;

select min(travel_time) min_, avg(travel_time) mean, max(travel_time) from all_quant_times;

---------------------------------------------------------------------------------------------------------------------------------------------

select * from all_agg_directness limit 10;

create temp table if not exists agg_direct_no_nulls as (select * from all_agg_directness where u_1_direct is not null and d_1_direct is not null and u_2_direct is not null and d_2_direct is not null)

select avg(u_1_direct) u1, avg(d_1_direct) d1, avg(u_2_direct) u2, avg(d_2_direct) d2 from agg_direct_no_nulls;


-- find dramatic changes in directness for plotting of routes





