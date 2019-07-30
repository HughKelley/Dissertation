







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


hugh

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