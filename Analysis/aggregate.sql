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











