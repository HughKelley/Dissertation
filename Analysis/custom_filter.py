# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:10:38 2019

@author: Hugh
"""


#import osmnx as ox



ox.config(use_cache=True, log_console=True)




filter_string = ('["area"!~"yes"]["highway"!~"footway|steps|corridor|motor|proposed|construction|abandoned|platform|raceway"]'
                    '["bicycle"!~"no"]["service"!~"private"]{}').format(settings.default_access)



#
#'["area"!~"yes"]
#["highway"!~"footway|steps|corridor|motor|proposed|construction|abandoned|platform|raceway"]'
#                    '["bicycle"!~"no"]["service"!~"private"]{}'
# !~ is the negation operator. 
# this query works by selecting all stuff that is not an area, is a highway that is not one of those things, 
# is not labelled no bicycle and is not private. 

#default_access = '["access"!~"private"]'


#
# query_template = '[out:json][timeout:{timeout}]{maxsize};({infrastructure}{filters}(poly:"{polygon}");>;);out;'
# query_str = query_template.format(polygon=polygon_coord_str, infrastructure=infrastructure, filters=osm_filter, timeout=timeout, maxsize=maxsize)


#def osm_net_download(polygon=None, north=None, south=None, east=None, west=None,
#                     network_type='all_private', timeout=180, memory=None,
#                     max_query_area_size=50*1000*50*1000, infrastructure='way["highway"]',
#                     custom_filter=None):


filter_string = 'blank'

