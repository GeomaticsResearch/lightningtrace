import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()
import shapely
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import _cntr as cntr
import lightningtrace
import os.path
import rasterio
import matplotlib
import fiona
import geopandas as gp

with rasterio.open(os.path.join('data', 'dem.img'), 'r') as rast:

    print rast.bounds

    subset = lightningtrace.utils.subset_raster(rast, 1, bbox=((299000, 128000, 300000, 129300)))
    band = subset['array']
    affine = subset['affine']

    bbox_px_coords = np.array(([0, 0],
     [0, rast.height],
     [rast.width, rast.height],
     [rast.width, 0]))

    #print lightningtrace.transformations.pixel_to_world_coords(rast.affine, bbox_px_coords)
    origin = 298085, 130585

    rast_y, rast_x = np.mgrid[:band.shape[0], :band.shape[1]]
    world_x, world_y = affine * (rast_x, rast_y)
    c = cntr.Cntr(world_x, world_y, band)

    contours = list()
    contours_to_create = [1080, 1070, 1060, 1050, 1040, 1030, 1020, 1010]
    for celev in contours_to_create:
        contour_res = c.trace(celev)
        nseg = len(contour_res) // 2
        segments, codes = contour_res[:nseg], contour_res[:nseg]
        seg_geom = [shapely.geometry.linestring.LineString(seg) for seg in segments]
        contours.append((celev, seg_geom))

    elev = list()
    geoms = list()
    for x in contours:
        for g in x[1]:
            elev.append(x[0])
            geoms.append(g)
    df = gp.GeoDataFrame({'elev': elev}, geometry=gp.GeoSeries(geoms, crs=rast.crs))
    df.to_file('contours.shp')


