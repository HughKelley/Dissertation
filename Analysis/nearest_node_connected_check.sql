---- for calculating the distance between nearest nodes and centroids

select * from nearest_node limit 1;
-- nearest node column is called 'nearest_common_node'
select * from unconnected_london_bike_1_projected_nodes limit 1;

create temp table unconnected_nn as (select a.nearest_common_node, b.osmid from nearest_node a left join unconnected_london_bike_1_projected_nodes b on a.nearest_common_node = b.osmid where b.osmid is null);



create temp table unconnected_nodes as (select a.nearest_common_node from nearest_node a left join unconnected_london_bike_1_projected_nodes b on a.nearest_common_node = b.osmid);

drop table unconnected_nodes;

select * from unconnected_nodes;
select count(*) from unconnected_nodes;

select count(*) from unconnected_nodes where nearest_common_node is not null;


SELECT
    a.id id_a,
    a.fruit fruit_a,
    b.id id_b,
    b.fruit fruit_b
FROM
    basket_a a
LEFT JOIN basket_b b ON a.fruit = b.fruit
WHERE b.id IS NULL;