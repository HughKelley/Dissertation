-- DROP TABLE osm_nodes;
-- DROP TABLE osm_tags;
-- DROP TABLE osm_way_tags;
-- Drop TABLE osm_ways;



-- SELECT COUNT(DISTINCT "value" ) FROM osm_way_tags;

-- SELECT COUNT(DISTINCT "key") FROM osm_way_tags;
-- SELECT * from osm_way_tags LIMIT 10;

-- SELECT DISTINCT "value" from osm_way_tags WHERE "key" = 'maxspeed';

-- SELECT COUNT(*) from osm_way_tags WHERE "key" = 'maxspeed';

-- SELECT * from lsoa_table LIMIT 5;

CREATE INDEX ind on lsoa_table ["LSOA11CD"];




-- DROP INDEX public.ind;

CREATE INDEX ind
    ON public.lsoa_table USING btree
    ("LSOA11CD" COLLATE pg_catalog."default" varchar_ops)
    TABLESPACE pg_default;

COMMENT ON INDEX public.ind
    IS 'just a test';