# convert network from multidigraph to multigraph, losing directional component and save to a pickle

import pickle

import networkx
import osmnx as ox 
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

def wkb_hexer(line):
    return line.wkb_hex

# convert geometry to usable type
def geom_column_to_wkb(gdf):

	gdf['geom'] = gdf['geometry'].apply(wkb_hexer)
	gdf.drop('geometry', 1, inplace=True)

	return gdf


crs = str(32230)

for key in range(1, 6):

	print(key)

	all_name = 'pickles/london_bike_' + str(key) + '_projected_pickle.file'



	un_name = 'pickles/unconnected_london_bike_' + str(key) + '_projected_pickle.file'

	out_all_name = 'pickles/undirected_london_bike_' + str(key) + '_projected_pickle.file'

	out_un_name = 'pickles/undirected_unconnected_london_bike_' + str(key) + '_projected_pickle.file'

	# print(all_name)
	# print(un_name)
	# print(out_all_name)
	# print(out_un_name)

	all_net = pickle.load(open(all_name, 'rb'))

	und_all_net = networkx.to_undirected(all_net)

	nodes, edges = ox.graph_to_gdfs(und_all_net, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)

	nodes = geom_column_to_wkb(nodes)
	edges = geom_column_to_wkb(edges)

	name = 'undirected_all_bike_' + str(key) 

	nodes.to_sql((name + '_nodes') , engine, if_exists='fail', index=False)
	edges.to_sql((name + '_edges') , engine, if_exists='fail', index=False)

	with engine.connect() as conn, conn.begin():
		sql = 'ALTER TABLE ' + name + '_nodes' + ' ALTER COLUMN geom TYPE Geometry(Point, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		conn.execute(sql)

	with engine.connect() as conn, conn.begin():
		sql = 'ALTER TABLE ' + name + '_edges' + ' ALTER COLUMN geom TYPE Geometry(LineString, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		conn.execute(sql)

##############################################################################################################
	un_net = pickle.load(open(un_name, 'rb'))

	und_un_net = networkx.to_undirected(un_net)

	nodes, edges = ox.graph_to_gdfs(und_un_net, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)

	nodes = geom_column_to_wkb(nodes)
	edges = geom_column_to_wkb(edges)

	name = 'undirected_unconnected_bike_' + str(key)

	nodes.to_sql((name + '_nodes') , engine, if_exists='fail', index=False)
	edges.to_sql((name + '_edges') , engine, if_exists='fail', index=False)

	with engine.connect() as conn, conn.begin():
		sql = 'ALTER TABLE ' + name + '_nodes' + ' ALTER COLUMN geom TYPE Geometry(Point, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		conn.execute(sql)

	with engine.connect() as conn, conn.begin():
		sql = 'ALTER TABLE ' + name + '_edges' + ' ALTER COLUMN geom TYPE Geometry(LineString, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		conn.execute(sql)




	# pickle.dump(und_all_net, open(out_all_name, 'wb'))

	# un_net = pickle.load(open(un_name, 'rb'))

	# und_un_net = networkx.to_undirected(un_net)

	# pickle.dump(und_un_net, open(out_un_name, 'wb'))

	# print(type(all_net))
	# print(type(und_all_net))