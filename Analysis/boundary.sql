# get a boundary of london using lsoa polygons in postgis

SELECT * FROM lsoa_table LIMIT 2;



CREATE TABLE public.result_union as (SELECT St_SetSrid( ST_MakePolygon (St_ExteriorRing( St_union( (lsoa_table.geom)))),27700) AS poly_boundary from lsoa_table)

-- 12 m 29 s
-- returned NULL