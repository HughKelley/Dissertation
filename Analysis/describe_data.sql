-- DROP TABLE osm_nodes;
-- DROP TABLE osm_tags;
-- DROP TABLE osm_way_tags;
-- Drop TABLE osm_ways;



-- SELECT COUNT(DISTINCT "value" ) FROM osm_way_tags;

-- SELECT COUNT(DISTINCT "key") FROM osm_way_tags;
-- SELECT * from osm_way_tags LIMIT 10;

-- SELECT DISTINCT "value" from osm_way_tags WHERE "key" = 'maxspeed';

SELECT COUNT(*) from osm_way_tags WHERE "key" = 'maxspeed';