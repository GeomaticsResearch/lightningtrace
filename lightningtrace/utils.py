import numpy as np
from lightningtrace.transformations import world_to_pixel_coords


def seq(start, stop, step=1):
    """Generate a list of values between start and stop every step
    :param start: The starting value
    :param stop: The ending values
    :param step: The step size
    :return: List of steps
    """
    n = int(round((stop - start) / float(step)))
    if n > 1:
        return [start + step * i for i in range(n + 1)]
    else:
        return []


def subset_raster(rast, band=1, bbox=None, logger=None):
    """
    :param rast: The rasterio raster object
    :param band: The band number you want to contour. Default: 1
    :param bbox: The bounding box in which to generate contours.
    :param logger: The logger object to use for this tool
    :return: A dict with the keys 'raster', 'array', 'affine', 'min', and 'max'. Raster is the original rasterio object,
    array is the numpy array, affine is the transformation for the bbox, min/max are the min/max values within the bbox.
    """
    # Affine transformations between raster and world coordinates.
    # See https://github.com/sgillies/affine
    # See https://github.com/mapbox/rasterio/blob/master/docs/windowed-rw.rst
    a = rast.transform      # Convert from pixel coordinates to world coordinates
    reverse_affine = ~a  # Convert from world coordinates to pixel coordinates

    # Copy the metadata
    kwargs = rast.meta.copy()

    # Read the band
    if bbox is not None:
        bbox = list(bbox)
        if len(bbox) != 4:
            logger.error('BBOX is not of length 4. Should be (xmin, ymin, xmax, ymax)')
            raise ValueError('BBOX is not of length 4. Should be (xmin, ymin, xmax, ymax)')

        # Restrict to the extent of the original raster if our requested
        # bbox is larger than the raster extent
        min_x = bbox[0]
        min_y = bbox[1]
        max_x = bbox[2]
        max_y = bbox[3]
        if min_x < rast.bounds[0]:
            min_x = rast.bounds[0]
        if min_y < rast.bounds[1]:
            min_y = rast.bounds[1]
        if max_x > rast.bounds[2]:
            max_x = rast.bounds[2]
        if max_y > rast.bounds[3]:
            max_y = rast.bounds[3]
        bbox = (min_x, min_y, max_x, max_y)

        # Convert the bounding box (world coordinates) to pixel coordinates
        # window = ((row_start, row_stop), (col_start, col_stop))
        window_bl = world_to_pixel_coords(rast.transform, [(bbox[0], bbox[1]),])
        window_tr = world_to_pixel_coords(rast.transform, [(bbox[2], bbox[3]),])

        window_rows = [int(window_bl[0, 1]), int(window_tr[0, 1])]
        window_cols = [int(window_bl[0, 0]), int(window_tr[0, 0])]

        window = (
          (min(window_rows), max(window_rows)),
          (min(window_cols), max(window_cols)))

        # print('')
        # print(window[0])
        # print(window[1])

        kwargs.update({
            'height': abs(window[0][1] - window[0][0]),
            'width': abs(window[1][1] - window[1][0]),
            'affine': rast.window_transform(window)
        })

    else:
        window = None

    # Read the data but only the window we set
    rast_band = rast.read(band, window=window, masked=True)
    rast_a = kwargs['affine']
    return {
        'crs': rast.crs,
        'array': rast_band,
        'affine': rast_a,
        'min': rast_band.min(),
        'max': rast_band.max()
    }
