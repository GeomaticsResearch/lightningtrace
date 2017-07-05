import logging
import shapely.speedups
if shapely.speedups.available:
   shapely.speedups.enable()
import shapely
from shapely.geometry import shape, mapping
import numpy as np
from matplotlib import _cntr as cntr
import rasterio

from lightningtrace.utils import subset_raster, seq


def _prepare_mpl_cntr(rast, band=1, bbox=None, logger=None):
    """
    :param rast: The rasterio raster object
    :param band: The band number you want to contour. Default: 1
    :param bbox: The bounding box in which to generate contours.
    :param logger: The logger object to use for this tool
    :return:
    """
    # Setup the logger
    logger = logger or logging.getLogger(__name__)

    subset_obj = subset_raster(rast, band, bbox, logger)
    rast_band = subset_obj['array']
    rast_a = subset_obj['affine']

    # We have to transpose the raster to match what matplotlib expects
    transpose_rast = np.transpose(rast_band)

    # Get the X and Y coordinates for the raster
    rast_x, rast_y = np.mgrid[:transpose_rast.shape[0], :transpose_rast.shape[1]]
    world_x, world_y = rast_a * (rast_x, rast_y)
    rast_x = None  # Clean up memory
    rast_y = None  # Clean up memory

    # Set up the contour object, this is an undocumented matplotlib class.
    c = cntr.Cntr(world_x, world_y, transpose_rast)
    world_x = None  # Clean up memory
    world_y = None  # Clean up memory
    return c


def _contour_mpl_worker(rast, contour_list, band=1, bbox=None, logger=None):
    """Contour a rasterio raster object for each elevation provided in contour_list. Returns a generator
    consisting of a tuple (contour elevation, list of Shapely linestring features)

    :param rast: The rasterio raster object
    :param contour_list: An iterable of values to contour
    :param band: The band number you want to contour. Default: 1
    :param bbox: The bounding box in which to generate contours.
    :param logger: The logger object to use for this tool
    :return: generator consisting of a tuple (contour elevation, list of Shapely linestring features)
    """
    # Setup the logger
    logger = logger or logging.getLogger(__name__)

    # Set up matplotlib for contouring
    c = _prepare_mpl_cntr(rast, band, bbox, logger=logger)

    # Now loop through each contour and contour that contour
    for contour_to_do in contour_list:
        yield list(_trace_mpl_contour(c, contour_to_do))


def _trace_mpl_contour(c_obj, contour_to_trace):
    """Trace a raster at the given elevation. Feed this function a matplotlib._cntr object and the elevation
    you want to trace. It yields a generator of tuples. The first object in the tuple is the elevation of the
    contour and the second object is the shapely geometry of that line segment.

    :param c_obj: The object produced by matplotlib._cntr
    :param contour_to_trace: The elevation to trace in the DEM
    :return: yields a generator of tuples. The first object in the tuple is the elevation of the
    contour and the second object is the shapely geometry of that line segment.
    """
    contour_res = c_obj.trace(contour_to_trace)
    nseg = len(contour_res) // 2
    segments, codes = contour_res[:nseg], contour_res[:nseg]
    seg_geom = [shapely.geometry.linestring.LineString(seg) for seg in segments]
    return contour_to_trace, seg_geom


def contour_dem(dem_fp, raster_band=1, min_val=None, max_val=None, method='basic', contour_interval=None,
                n_contours=None, contour_list=None, bbox=None, output_format='features', logger=None):
    """Contour the DEM using one of two approaches, export geojson.

    :param dem_fp: the filepath to the DEM you want to contour

    :param raster_band: The band number to read in. Default: 1

    :param min_val: The minimum elevation you want to contour. Default: DEM min

    :param max_val: The maximum elevation you want to contour. Default: DEM max

    :param method: the contouring method ('step', 'basic', or 'list'). Step generates n contours over the DEM vertical
    range. Basic generates contours every x vertical units. List generates the given contours.

    :param contour_interval: If method=='basic' you must provide this value. It is the vertical interval at which
    contours are places (i.e., every 10 ft)

    :param n_contours:: If method=='step' you must provide this value. It is the number of contours you want to
    generate over the range of DEM elevations (i.e., generate 10 contours over the range of elevations in the DEM)

    :param contour_list: If method=='list' you must provide this value. It provides a list of DEM values on which to
    contour. (i.e., generate contours at 3ft, 6ft, and 7ft)

    :param bbox: The bounding box in which to generate contours.

    :param output_format:

    :param logger: The logger object to use for this tool

    :return:Geopandas GeoDataFrame
    """
    # Sanitize the method parameter above
    method = method.lower()

    # Setup the logger
    logger = logger or logging.getLogger(__name__)

    logger.info("Contouring DEM...")
    if bbox:
        bbox = list(bbox)
        if len(bbox) != 4:
            logger.error('BBOX is not of length 4. Should be (xmin, ymin, xmax, ymax)')
            raise ValueError('BBOX is not of length 4. Should be (xmin, ymin, xmax, ymax)')

    # Open the DEM and get metadata
    with rasterio.open(dem_fp, 'r') as src:
        rast_crs = src.crs  # Get the CRS of the raster

        # Calculate min max if not set as a parameter
        if min_val is None or max_val is None:
            subset_obj = subset_raster(src, raster_band, bbox, logger)
            if min_val is None:
                min_val = subset_obj['min']
            if max_val is None:
                max_val = subset_obj['max']
            subset_obj = None

        if method == 'basic':
            if contour_interval is not None:
                if type(contour_interval) not in (float, int):
                    logger.error("you must supply a float or int as a contour interval for the basic contouring method")
                    raise ValueError("you must supply a float or int as a contour interval for the basic contouring method")
            else:
                logger.error("you must provide a contour interval for the basic contouring method")
                raise ValueError("you must provide a contour interval for the basic contouring method")
            n_contours = int((float(max_val) - float(min_val)) / float(contour_interval))
            contour_list = seq(min_val, max_val, contour_interval)
            logger.info("Using the 'basic' contouring method")
            logger.info("min h: {0}; max h: {1}; interval: {2}; n levels: {3}".format(
                    round(min_val, 2), round(max_val, 2), round(contour_interval, 2), n_contours))
            logger.info('contours: ')
            logger.info(contour_list)

        elif method == 'step':
            if (type(min_val) not in (float, int))\
                    or (type(max_val) not in (float, int))\
                    or (type(n_contours) not in (float, int)):
                logger.error("you must supply an int for parameter n_contours if running in 'step' mode")
                raise ValueError("you must supply an int for parameter n_contours if running in 'step' mode")
            contour_interval = (float(max_val) - float(min_val)) / float(n_contours)
            contour_list = seq(min_val, max_val, contour_interval)
            logger.info("Using the 'step' contouring method")
            logger.info("min h: {0}; max h: {1}; interval: {2}; n levels: {3}".format(
                    round(min_val, 2), round(max_val, 2), round(contour_interval, 2), n_contours))
            logger.info("Contours to generate: {0}".format(contour_list))

        elif method == 'list':
            if type(contour_list) not in (list, tuple):
                logger.error("you must supply a list or tuple of contours within parameter contour_list if running in 'list' mode")
                raise ValueError("you must supply a list or tuple of contours within parameter contour_list if running in 'list' mode")
            contour_interval = None
            n_contours = len(contour_list)
            logger.info("Using the 'list' contouring method")
            logger.info("min h: {0}; max h: {1}; interval: {2}; n levels: {3}".format(
                    round(min_val, 2), round(max_val, 2), contour_interval, n_contours))
            logger.info("Contours to generate: {0}".format(contour_list))

        else:
            logger.error("The contouring method '{0}' is not available. Please use 'basic', 'step', or 'list'".format(method))
            raise NotImplementedError("The contouring method '{0}' is not available. Please use 'basic', 'step', or 'list'".format(method))

        # Do the contouring
        contour_results = list(_contour_mpl_worker(src, contour_list, band=raster_band, bbox=bbox, logger=logger))

        # Now loop through each contour
        geojson = {
            'type': 'FeatureCollection',
            'features': list(),
            'crs_wkt': rast_crs
        }
        feat_i = 0
        for contour_elev, contour_geoms in contour_results:
            for geom in contour_geoms:
                geojson['features'].append({
                    'type': 'Feature',
                    'geometry': mapping(geom),
                    'properties': {
                        'ID': feat_i,
                        'elev': contour_elev,
                    }
                })
                feat_i += 1

        logger.info("Done contouring DEM.")
        if output_format.lower() == 'features':
            return geojson['features']
        elif output_format.lower() == 'collection':
            return geojson
        else:
            raise NotImplementedError("This output format is not supported. Please choose 'features' or 'collection' ")
