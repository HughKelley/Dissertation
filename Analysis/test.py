# test plotting in powershell

import osmnx as ox
ox.config(log_console=True, use_cache=True)
ox.__version__



place = 'Piedmont, California, USA'

gdf = ox.gdf_from_place(place)
gdf.loc[0, 'geometry']

# not plotted in powershell as it is in jupyter notebooks