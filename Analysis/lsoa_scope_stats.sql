-- get stats for the stuff going on within the north inner london boundary i"m using. 

select * from jtw limit 1;

select distinct origin_name from jtw;

select distinct destination_name from jtw;

select distinct travel_mode from jtw;

create temp table if not exists origin_subset as (select * from jtw where origin_name  in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster, City of London'));

create temp table if not exists destination_subset as (select * from jtw where destination_name  in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster, City of London'));

create temp table if not exists both_subset as (select * from jtw where origin_name in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster, City of London') and destination_name  in ('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster, City of London'));

--('Camden', 'Hackney', 'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Tower Hamlets', 'Westminster, City of London')

select * from origin_subset limit 1;

select sum(value) from jtw;
select sum(value) from origin_subset;
select sum(value) from destination_subset;
select sum(value) from both_subset;

select sum(value) from jtw where travel_mode = 'Bicycle';
select sum(value) from origin_subset where travel_mode = 'Bicycle';
select sum(value) from destination_subset where travel_mode = 'Bicycle';
select sum(value) from both_subset where travel_mode = 'Bicycle';


select * from casualties limit 1;
select count(*) from casualties;

select distinct casualties."Borough" from casualties;

select count(*) from casualties where "Borough" in ('CAMDEN','TOWER HAMLETS','CITY OF LONDON','HAMMERSMITH & FULHAM','WESTMINSTER','HACKNEY','KENSINGTON & CHELSEA','ISLINGTON');


select count(*) from lsoa_table;
-- 4879
select count(*) from north_inner_subset;
-- 894



