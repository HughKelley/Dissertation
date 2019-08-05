-- Raw data tables are:

-- lsoa_table
-- casualties
-- edges
-- nodes
-- journey to work
-- quant


-- Tasks
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- clean up DB

--london_all_edges, london_all_nodes, london_bike_edges, london_bike_nodes, london_drive_edges, london_drive_nodes, london_drive_projected_edges, london_drive_projected_nodes, london_walk_edges, london_walk_nodes
drop table if exists london_all_edges, london_all_nodes, london_bike_edges, london_bike_nodes, london_drive_edges, london_drive_nodes, london_drive_projected_edges, london_drive_projected_nodes, london_walk_edges, london_walk_nodes;

-- drop osm tables
drop table if exists osm_nodes, osm_tags, osm_ways, osm_way_tags;

-- old subsets
drop table if exists north_inner_subset, lsoa_subset;

-- old boundaries
drop table if exists geo_crs_lbound, geo_north_inner_bound, inner_london_boundary;


-- check lsoa table multipolygons in QGIS
-- drop table multipolygon_lsoas;
-- instead of defining this table explicitly, easier to build it from the select statement
-- create table if not exists multipolygon_lsoas (like lsoa_table);
select * from lsoa_table limit 1;
create temp table if not exists multi as select "LSOA11CD", count("LSOA11CD") from lsoa_table group by "LSOA11CD" having count("LSOA11CD") > 1;

create table if not exists multi_polygon_lsoas as select multi."LSOA11CD" as lsoa11cd, "LSOA11NM" as lsoa11nm, geom  from multi left join lsoa_table on multi."LSOA11CD" = lsoa_table."LSOA11CD";

-- and then inspect this in QGIS ot understand why these are multipolygons

---- build table of lsoa's with small parts cleaned out
--create table clean_lsoa as table lsoa_subset;
---- delete row where area is less 
--delete from clean_lsoa a using clean_lsoa b where a.area < b.area and a.lsoa11cd = b.lsoa11cd;
----check number of rows
--select count(*) from clean_lsoa;

-- build north inner london subset
create table if not exists north_inner_subset (like lsoa_table);
insert into north_inner_subset(select * from lsoa_table where "LAD11NM" in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster', 'City of London'));

-- calculate lsoa polygon area column

-- calculate a boundary around the north inner london subset
create table if not exists boundaries (
	id integer ,
	b_name text,
	geom geometry,
	constraint p_key primary key (id)
	);

insert into boundaries(id, b_name, geom) values (1, 'inner_north_london', (select ST_UNION(geom) from north_inner_subset));

-- inner london boundary
create temp table if not exists inner_subset as select * from lsoa_table where "LAD11NM" in ('Camden', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Lambeth', 'Lewisham', 'Southwark', 'Tower Hamlets', 'Wandsworth', 'Westminster', 'City of London');
insert into boundaries(id, b_name, geom) values (2, 'inner_london', (select ST_union(geom) from inner_subset));
-- london boundary
insert into boundaries(id, b_name, geom) values (3, 'london', (select ST_union(geom) from public.lsoa_table));

-- do boundaries in QGIS, then ST_Dump them into component polygons and select the largest one. 
create temp table if not exists north_inner_dissolved as select st_dump(geom) from "Dissolved";

-- 'Delete Holes' in QGIS

-- check the output
--to check proj support is installed
select postgis_full_version();
select * from cleaned limit 1;
select st_srid(geom) from cleaned;
select find_srid('public', 'cleaned', 'geom');

-- its BNG 27700 so convert to wsg84 4326 in a new table

create table if not exists wsg_clean_boundary as select id, st_transform(geom, 4326) as geom from cleaned;

-- delete polygons where the id is not unique and the area is less
alter table north_inner_subset add column area double precision;
update north_inner_subset set area=st_area(geom);

-- check the column names
select * from north_inner_subset limit 1;

select st_exteriorring(geom) from boundaries;

-- then delete small polygons
delete from north_inner_subset a using north_inner_subset b where a.area < b.area and a."LSOA11CD"= b."LSOA11CD";

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- in python, use the wsg84 boundary calculated to grab networks from OSM

-- index necessary columns

-- then calcualate descriptive statistics


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- add primary key to wsg_clean_boundary

alter table wsg_clean_boundary add column p_key serial primary key;
alter table wsg_clean_boundary rename column "st_transform" to geom;
select * from wsg_clean_boundary;


select st_extent(geom) from wsg_clean_boundary;






select version();
--------------------------------------------------------------------------------------------------------------

select distinct highway, count(highway) from london_bike_1_projected_edges group by highway;

--drop table relation_edges;
select count(*) from relation_edges;

select st_srid(geom) from london_bike_1_projected_edges;
select find_srid('public', 'london_bike_1_projected_edges', 'geom');

select count(*) from clipped_relation_edges;
-- transform to UTM 30 or BNG...

-- saet correct srid

alter table london_bike_5_projected_edges alter column geom type geometry(LineString, 32230) using st_setsrid(geom::Geometry, 32230);
alter table london_bike_5_projected_nodes alter column geom type geometry(Point, 32230) using st_setsrid(geom::Geometry, 32230);



select st_srid(geom) from cleaned;
select find_srid('public', 'cleaned', 'geom');

--describe_data.sql

-- DROP TABLE osm_nodes;
-- DROP TABLE osm_tags;
-- DROP TABLE osm_way_tags;
-- Drop TABLE osm_ways;

drop table london_bike_5_projected_edges;
drop table london_bike_5_projected_nodes;

drop table london_basic_bike_projected_edges;
drop table london_basic_bike_projected_nodes;

-- SELECT COUNT(DISTINCT "value" ) FROM osm_way_tags;

-- SELECT COUNT(DISTINCT "key") FROM osm_way_tags;
-- SELECT * from osm_way_tags LIMIT 10;

-- SELECT DISTINCT "value" from osm_way_tags WHERE "key" = 'maxspeed';

-- SELECT COUNT(*) from osm_way_tags WHERE "key" = 'maxspeed';

-- SELECT * from lsoa_table LIMIT 5;
--
--CREATE INDEX ind on lsoa_table ["LSOA11CD"];
--

---- DROP INDEX public.ind;
--
--CREATE INDEX ind
--    ON public.lsoa_table USING btree
--    ("LSOA11CD" COLLATE pg_catalog."default" varchar_ops)
--    TABLESPACE pg_default;
--
--COMMENT ON INDEX public.ind
--    IS 'just a test';
   
select count(*) from jtw;

select * from jtw limit 10;


-- Journey to work stats
select origin_name, sum(value) as total from jtw group by origin_name;
select destination_name, sum(value) as total from jtw group by destination_name;
select travel_mode, sum(value) as total from jtw group by travel_mode;

select distinct origin_name from jtw;
select distinct travel_mode from jtw;


select origin_name, sum(value) as total from jtw where origin_name in (
	'Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster,City of London') group by origin_name;


select destination_name, sum(value) as total from jtw where destination_name in 
	('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster,City of London') 
	and origin_name in 
	('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster,City of London') 
	and travel_mode in ('Bicycle')
	group by destination_name;


--------------------------------------
-- clean and clip KSI data

select * from casualties limit 10;

--convert easting and northing column to point geometry

-- crs is bng 27700


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--centroid.sql

--SELECT * FROM lsoa_table LIMIT 10;

-- test it out
-- SELECT ST_centroid(geom) from lsoa_table LIMIT 10;

-- ALTER TABLE lsoa_table ADD COLUMN center GEOMETRY;

-- UPDATE lsoa_table SET center = ST_Centroid(geom);


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--clean_up.sql

-- Select COUNT(*) from osm_tags LIMIT 10;
-- Select COUNT(*) from osm_elements LIMIT 10;
--
--DROP TABLE osm_elements;
--DROP TABLE osm_tags;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

--test.sql
-- SELECT * from  LIMIT 10;
-- DROP TABLE IF EXISTS test, ;
-- ALTER TABLE "QUANT" RENAME TO quant;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

--select distinct "LAD11NM" from public.lsoa_table;

--SET search_path TO public;

--SELECT "LSOA11CD", "LSOA11NM", "MSOA11CD", "MSOA11NM", "LAD11CD", "LAD11NM", "RGN11CD" FROM public.lsoa_table limit 10;

--create table if not exists lsoa_subset (like lsoa_table);

--insert into lsoa_subset(select * from lsoa_table where "LAD11NM" in ('Camden', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Lambeth', 'Lewisham', 'Southwark', 'Tower Hamlets', 'Wandsworth', 'Westminster', 'City of London'));

--create table if not exists inner_london_boundary (
--	id integer ,
--	geom geometry
--	);


--insert into inner_london_boundary(id, geom) values (1, (select ST_Union(geom) from lsoa_subset));

--insert into geo_crs_lbound(select id, st_transform(geom, 4326) from public.inner_london_boundary);

ALTER TABLE public.geo_crs_lbound ADD "name" varchar NULL;

--make inner london boroughs north of the river subset

--create table if not exists north_inner_subset (like lsoa_table);

select count(*) from lsoa_subset limit 1;

insert into north_inner_subset(select * from lsoa_table where "LAD11NM" in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster', 'City of London'));

insert into inner_london_boundary(id, geom) values (3, (select ST_UNION(geom) from north_inner_subset));

select distinct "LAD11NM" from lsoa_table;

select * from london_bike_nodes limit 200;

--select postgis_full_version();


--

--
--

--create table if not exists jtw_data(
--	index integer,
--	geography varchar(15),
--	geography_code varchar(15),
--	rural-urban varchar(20),
--	method_all integer,	
--)


--select ST_SRID(geom) from public.inner_london_boundary;

-- these seemed to hang, several minutes...
--alter table inner_london_boundary add column wsg_boundary geometry(Geometry, 4326) ;
--ALTER TABLE public.inner_london_boundary ADD wsg84_geom geometry NULL;


-- it isn't a big table
--select count(*) from public.inner_london_boundary;

--so make new table and insert after transforming instead. 


--create table if not exists geo_crs_lbound (
--	id integer not null,
--	geom geometry,
--	constraint p_key primary key (id)
--) 

create table if not exists geo_north_inner_bound (like geo_crs_lbound);


insert into geo_north_inner_bound (select id, st_transform(geom, 4326) from public.north_inner_subset);

select * from inner_london_boundary;
select * from geo_crs_lbound;

SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';

select * from lsoa_subset limit 2000;

select count(*) from london_all_edges;

alter table london_walk_edges alter column geom type geometry(Linestring, 27700) using ST_Transform(geom, 27700);
alter table london_walk_nodes alter column geom type geometry(Point, 27700) using ST_Transform(geom, 27700);



--drop table public.nearest_node;

create table if not exists public.nearest_node (
	id serial primary key,
	lsoa_id text,
	lsoa_centroid geometry,
	nearest_bike_node int8,
	nearest_all_node int8,
	nearest_drive_node int8,
	nearest_walk_node int8
	)
	
	
select * from lsoa_subset limit 1;
	
insert into public.nearest_node (lsoa_id, lsoa_centroid) 
	select "LSOA11CD", center from lsoa_subset;

select count(*), count(distinct "LSOA11CD") from lsoa_subset;
--  looks like there were 11 lsoas with multipolygon dimensions

select "LSOA11CD", count("LSOA11CD") from lsoa_subset group by "LSOA11CD" having count("LSOA11CD") > 1;

--'E01003236', 'E01033730', 'E01032834', 'E01000928', 'E01004596', 'E01004015', 'E01003199', 'E01032775', 'E01033740', 'E01032783', 'E01032739'
	
-- add primary key to lsoa_subset
alter table lsoa_subset add column id serial primary key;
select * from lsoa_subset limit 2;
-- add area column to lsoa_subset
alter table lsoa_subset add column area double precision;
--ALTER TABLE public.lsoa_subset ALTER COLUMN area TYPE double precision USING area::double precision;

update lsoa_subset set area=ST_AREA(geom);
-- update 1620 rows, 
select count(*) from lsoa_subset;
-- that's the correct number of row

insert into lsoa_subset (area) values ST_area(geom);

--to aoid having to use ""
ALTER TABLE public.lsoa_subset RENAME COLUMN "LSOA11CD" TO lsoa11cd;

--create copy table for safety

create table clean_lsoa as table lsoa_subset;

-- delete row where area is less 
delete from clean_lsoa a using clean_lsoa b where a.area < b.area and a.lsoa11cd = b.lsoa11cd;

--check number of rows
select count(*) from clean_lsoa;

--now pass that data into the nearest node table
insert into public.nearest_node (lsoa_id, lsoa_centroid) select lsoa11cd, center from clean_lsoa;

--insert into the other column the node from the node table that's closest to the center point.

--create index to speed up <->
create index london_all_nodes_gix on london_all_nodes using GIST (geom);
create index london_all_edges_gix on london_all_edges using GIST (geom);

--This was the wrong thing to do, should be update, not insert. update adds columns insert adds rows
--INSERT INTO nearest_node (nearest_drive_node) SELECT osmid FROM london_drive_nodes ORDER BY nearest_node.lsoa_centroid <->  london_drive_nodes.geom LIMIT 1;
--SQL Error [42P01]: ERROR: invalid reference to FROM-clause entry for table "nearest_node"
--  Hint: There is an entry for table "nearest_node", but it cannot be referenced from this part of the query.



select distinct highway from london_bike_edges;
select distinct highway from london_bike_nodes;
--84 values, but some are combinations of multiple values so fewer than that
--https://wiki.openstreetmap.org/wiki/Tags

--drive
--bike
--walk
--all


select * from  london_all_nodes limit 1;
select * from london_drive_nodes limit 1;
select * from london_drive_projected_nodes limit 1;




select distinct highway from london_all_edges;
select distinct highway from london;


select count(*) from north_inner_subset;