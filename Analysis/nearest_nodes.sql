-- get the node nearest to centrepoint of each LSOA from the fully connected bike_1 network 
-- and calculate the distance between the node and the centrepoint


drop table nearest_node_temp;

create temp table if not exists nearest_node_temp as (
	select "LSOA11CD" as lsoa11cd, "LAD11NM" as lad11nm, geom, centroid from north_inner_subset
);


select * from nearest_node_temp limit 1;

alter table nearest_node_temp add column nearest_common_node bigint;

--create index london_all_nodes_gix on london_all_nodes using GIST (geom);

create index centroid_node_gix on nearest_node_temp using GIST(centroid);

select * from unconnected_london_bike_1_projected_nodes limit 1;
create index uncon_1_node_gix on unconnected_london_bike_1_projected_nodes using GIST(geom);




UPDATE nearest_node_temp
SET nearest_common_node = (
  SELECT a.osmid
  FROM unconnected_london_bike_1_projected_nodes a
  ORDER BY nearest_node_temp.centroid <-> a.geom
  LIMIT 1
);

select * from nearest_node_temp limit 1;

select * from unconnected_london_bike_1_projected_nodes limit 1;

create temp table nearest_node_temp_both as (
select 
	a.lsoa11cd lsoa11cd, 
	a.lad11nm lad11nm, 
	a.geom as poly_geom, 
	a.centroid centroid, 
	a.nearest_common_node nearest_common_node, 
	b.geom as node_geom
from 
	nearest_node_temp a
left join unconnected_london_bike_1_projected_nodes b on a.nearest_common_node = b.osmid);

--alter table nearest_node_temp add column distance float;

--select * from nearest_node_temp limit 1;

select *, st_distance(centroid, node_geom) from nearest_node_temp_both;

create table nearest_node as (select *, st_distance(centroid, node_geom) as distance from nearest_node_temp_both);

select * from nearest_node limit 1;

alter table nearest_node rename column st_distance to distance;

select max(distance) from nearest_node;


