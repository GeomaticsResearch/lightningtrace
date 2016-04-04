import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()
import shapely
import numpy as np
from matplotlib import _cntr as cntr

def extract_contours(band, affine, contours):
    """Contour the DEM for the contours given by variable contours and yield an iterable of GeoJson features.

    :param band: A rasterio/numpy vector representing the DEM
    :param affine: The affine transformation that relates pixel to world coordinates.
    :param contours: A iterable of contour elevations to trace
    :return: generator of GeoJSON features
    """
    # Setup the matplotlib tracing object
    rast_y, rast_x = np.mgrid[:band.shape[0], :band.shape[1]]
    world_x, world_y = affine * (rast_x, rast_y)
    c = cntr.Cntr(world_x, world_y, band)

    # Build the contours, yield a feature for each one
    for contour_elev in contours:
        contour_res = c.trace(contour_elev)
        nseg = len(contour_res) // 2
        segments, codes = contour_res[:nseg], contour_res[:nseg]
        for seg in segments:
            yield {
                'type': 'Feature',
                'geometry': shapely.geometry.geo.mapping(shapely.geometry.linestring.LineString(seg)),
                'properties': {
                    'elev': contour_elev
                }}