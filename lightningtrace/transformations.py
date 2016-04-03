import numpy as np


def world_to_pixel_coords(affine, coords):
    """Convert a set of coordinates from world to pixel coordinates.

    :param affine: The rasterio affine object
    :param coords: World coordinates you want to translate to pixel coordinates
    """
    # Affine transformations between raster and world coordinates.
    # See https://github.com/sgillies/affine
    # See https://github.com/mapbox/rasterio/blob/master/docs/windowed-rw.rst
    # See http://www.perrygeo.com/python-affine-transforms.html
    # affine = Convert from pixel coordinates to world coordinates
    reverse_affine = ~affine  # reverse_affine = Convert from world coordinates to pixel coordinates

    col, row = reverse_affine * (coords[0], coords[1])
    return col, row


def pixel_to_world_coords(affine, pixel_coords):
    """Convert a set of coordinates from pixel to world coordinates.

    :param affine: The rasterio affine object
    :param pixel_coords: Pixel coordinates (col, row) you want to translate to world coordinates
    """
    # Affine transformations between raster and world coordinates.
    # See https://github.com/sgillies/affine
    # See https://github.com/mapbox/rasterio/blob/master/docs/windowed-rw.rst
    # See http://www.perrygeo.com/python-affine-transforms.html
    # affine = Convert from pixel coordinates to world coordinates
    reverse_affine = ~affine  # reverse_affine = Convert from world coordinates to pixel coordinates

    X, Y = affine * (pixel_coords[0], pixel_coords[1])
    return X, Y