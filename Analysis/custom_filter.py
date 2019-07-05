# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:10:38 2019

@author: Hugh
"""


import osmnx as ox
ox.config(use_cache=True, log_console=True)




filter_string = ('["area"!~"yes"]["highway"!~"footway|steps|corridor|motor|proposed|construction|abandoned|platform|raceway"]'
                    '["bicycle"!~"no"]["service"!~"private"]{}').format(settings.default_access)


filter_string = 'blank'

