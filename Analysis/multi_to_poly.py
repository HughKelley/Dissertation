import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

def explode(indata):
    count_mp = 0
    indf = gpd.GeoDataFrame.from_file(indata)
    outdf = gpd.GeoDataFrame(columns=indf.columns)
    for idx, row in indf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row,ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            count_mp = count_mp + 1
            multdf = gpd.GeoDataFrame(columns=indf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs,ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom,'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf,ignore_index=True)
    print("There were ", count_mp, "Multipolygons found and exploded")
    return outdf


if __name__ == '__main__':

    print('ok')

    file = "C:/Users/Hugh/Documents/UCL_CASA_1819/Dissertation/Analysis/Data/diss_north_inner.shp"
    poly_gdf = explode(file)

    test = poly_gdf.to_file('split_boundary.shp')