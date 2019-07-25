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

select ST_SRID(geom) from public.inner_london_boundary;
