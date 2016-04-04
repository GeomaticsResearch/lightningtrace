import numpy as np

def world_to_pixel_coords(affine, coords):
    """Convert a set of coordinates from world to pixel coordinates.

    :param affine: The rasterio affine object
    :param coords: World coordinates you want to translate to pixel coordinates
    """
    # Convert to numpy array
    coords = np.array(coords)
    if coords.shape[0] <= 0 or coords.shape[1] < 2:
        raise ValueError("Shape of coords is incorrect. Please make sure you have X, Y, optional Z format")

    # Affine transformations between raster and world coordinates.
    # See https://github.com/sgillies/affine
    # See https://github.com/mapbox/rasterio/blob/master/docs/windowed-rw.rst
    # See http://www.perrygeo.com/python-affine-transforms.html
    # affine = Convert from pixel coordinates to world coordinates
    reverse_affine = ~affine  # reverse_affine = Convert from world coordinates to pixel coordinates
    coords[:, 0:2] = np.apply_along_axis(lambda x: reverse_affine*(x[0], x[1]), axis=1, arr=coords)
    return coords


def pixel_to_world_coords(affine, pixel_coords):
    """Convert a set of coordinates from pixel to world coordinates.

    :param affine: The rasterio affine object
    :param pixel_coords: Pixel coordinates (col, row) you want to translate to world coordinates
    """
    coords = np.array(pixel_coords)
    if coords.shape[0] <= 0 or coords.shape[1] < 2:
        raise ValueError("Shape of pixel_coords is incorrect. Please make sure you have X, Y, optional Z format")
    # Affine transformations between raster and world coordinates.
    # See https://github.com/sgillies/affine
    # See https://github.com/mapbox/rasterio/blob/master/docs/windowed-rw.rst
    # See http://www.perrygeo.com/python-affine-transforms.html
    # affine = Convert from pixel coordinates to world coordinates
    reverse_affine = ~affine  # reverse_affine = Convert from world coordinates to pixel coordinates
    coords[:, 0:2] = np.apply_along_axis(lambda x: affine*(x[0], x[1]), axis=1, arr=coords)
    return coords
