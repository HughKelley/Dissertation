# get london's cycleways

import osmnx as ox 

ox.config(use_cache=True, log_console=True)

cycle_filter = '["area"!~"yes"]["highway"="cycleway"]'

london = ox.graph_from_place('London, United Kingdom', network_type='bike', retain_all = True, name = 'london_cycle', which_result=2, custom_filter = cycle_filter)


fig, ax = ox.plot_graph(london)

# this returns a good network




bridleway
corridor
cycleway
elevator
escalator
footway
highway
living_street
no
path
ped
pedestrian
primary
primary_link
residential
road
secondary
secondary_link
service
services
steps
tertiary
tertiary_link
track
trunk
trunk_link
unclassified
unsurfaced
https://wiki.openstreetmap.org/wiki/Highway_tagging_samples
