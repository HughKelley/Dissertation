--select distinct "LAD11NM" from public.lsoa_table;




--SET search_path TO public;

--SELECT "LSOA11CD", "LSOA11NM", "MSOA11CD", "MSOA11NM", "LAD11CD", "LAD11NM", "RGN11CD" FROM public.lsoa_table limit 10;

--create table if not exists lsoa_subset (like lsoa_table);

--insert into lsoa_subset(select * from lsoa_table where "LAD11NM" in ('Camden', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Lambeth', 'Lewisham', 'Southwark', 'Tower Hamlets', 'Wandsworth', 'Westminister', 'City of London'));

--select postgis_full_version();

--create table if not exists inner_london_boundary (
--	id integer ,
--	geom geometry
--	);
--
--insert into inner_london_boundary(id, geom) values (1, (select ST_Union(geom) from lsoa_subset));
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


--insert into geo_crs_lbound(select id, st_transform(geom, 4326) from public.inner_london_boundary);

select * from inner_london_boundary;
select * from geo_crs_lbound;

SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';

select * from lsoa_subset limit 20;
