-----   prepping data for histograms

select * from o_d_points_aggregate limit 10;

drop table node_centroid_dist_diffs;

create table if not exists node_centroid_dist_diffs as (
	select 
		node_dist - centroid_dist as differences
	from 
		o_d_points_aggregate 
	where
		quant_origin_code != quant_dest_code
);

select * from node_centroid_dist_diffs limit 10;



drop table primary_trunk_net;