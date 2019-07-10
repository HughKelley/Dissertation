# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:02:56 2019

@author: Hugh
"""

import geopandas as gpd

file = "Data/statistical-gis-boundaries-london/ESRI\LSOA_2011_London_gen_MHW.shp"
shapefile = gpd.read_file(file)
print(shapefile)