SELECT * FROM lsoa_table LIMIT 10;

-- test it out
-- SELECT ST_centroid(geom) from lsoa_table LIMIT 10;

-- ALTER TABLE lsoa_table ADD COLUMN center GEOMETRY;

-- UPDATE lsoa_table SET center = ST_Centroid(geom);
