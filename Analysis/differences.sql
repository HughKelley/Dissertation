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



