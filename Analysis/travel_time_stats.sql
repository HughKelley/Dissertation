select avg(distance) from travel_times_2;
select min(distance) from travel_times_2;
select max(distance) from travel_times_2;
select stddev(distance) from travel_times_2;

select count(*) from travel_times_1;
-- 797,450
select count(*) from undirected_travel_times_1;
-- 684,166

select count(*) from travel_times_2;
-- 797,450
select count(*) from undirected_travel_times_2;
-- 684,166

select count(*) from nearest_node;
-- 894
-- 799236 - 89

--create table of cross joined inner nodes
--check exactly which pairs are mising from full tables
--check which pairs are missing from incomplete table
--match values to column
--group by origin and destination