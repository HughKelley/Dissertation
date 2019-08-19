-- groupings
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------

create table if not exists 
	group_origin_time_count 
as (
	select quant_origin, count(u_2_time) u_2_counts, count(d_2_time) d_2_counts, count(quant_time) quant_count from all_agg_times group by quant_origin
);

select * from all_agg_times;

select * from group_origin_time_count;

select distinct u_2_counts from group_origin_time_count;
--8 rows fetched


select distinct d_2_counts from group_origin_time_count;
--14 rows fetched

select * from all_agg_times limit 1;

create table if not exists
	group_origin_time_mean
as (
	select 
		quant_origin, 
		avg(u_1_time) u_1_mean, 
		avg(d_1_time) d_1_mean,
		avg(u_2_time) u_2_mean, 
		avg(d_2_time) d_2_mean, 
		avg(quant_time) quant_mean, 
		avg(quant_time_plus) quant_plus_mean 
	from 
		all_agg_times 
	group by 
		quant_origin
);

select * from group_origin_time_mean;


-------------------------------------------------------------------------------------------------------------------------------------------

--remove rows with null in any column

select * from all_agg_times limit 1;

create temp table if not exists 
	temp_agg_times_no_nulls 
as (
select 
		*
	from 
		all_agg_times 
	where 
		origin_node is not null 
		and
		dest_node is not null 
		and
		quant_dest is not null 
		and 
		quant_origin is not null 
		and
		u_1_time is not null 
		and
		d_1_time is not null 
		and
		u_2_time is not null 
		and
		d_2_time is not null 
		and
		quant_time is not null 
		and
		quant_time_plus is not null
);

-- 341,935 pairs where none of the rows are null. 

create table if not exists agg_times_no_nulls as (select * from temp_agg_times_no_nulls)

select * from agg_times_no_nulls limit 1;

create table if not exists net_stats as (
select 'u_1' as net, avg(u_1_time), min(u_1_time), max(u_1_time), stddev_samp(u_1_time) stdev from agg_times_no_nulls
union
select 'd_1' as net, avg(d_1_time), min(d_1_time), max(d_1_time), stddev_samp(d_1_time) stdev from agg_times_no_nulls
union
select 'u_2' as net, avg(u_2_time), min(u_2_time), max(u_2_time), stddev_samp(u_2_time) stdev from agg_times_no_nulls
union
select 'd_2' as net, avg(d_2_time), min(d_2_time), max(d_2_time), stddev_samp(d_2_time) stdev from agg_times_no_nulls
union
select 'quant' as net, avg(quant_time), min(quant_time), max(quant_time), stddev_samp(quant_time) stdev from agg_times_no_nulls
union
select 'quant_time_plus' as net, avg(quant_time_plus), min(quant_time_plus), max(quant_time_plus), stddev_samp(quant_time_plus) stdev from agg_times_no_nulls
);

--drop table net_stats;

select net, min, avg as mean, max, stdev as st_dev from net_stats;




--  matrix of changes in directness

-- count nulls in each column
-- create temp table of no nulls
--calc difference in avg directeness between pair

	
select * from quant limit 1;

select count(*) from quant where origin != destination and travel_time_mins = 0;



