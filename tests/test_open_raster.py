import pytest

@pytest.yield_fixture
def dem_rast():
    """Open the test DEM as a fixture"""
    import os.path
    import rasterio
    with rasterio.open(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data', 'dem.img'), 'r') as rast:
        yield rast

def test_rast_affine_object(dem_rast):
    """
    Open a raster. This test should be covered by rasterio library but we'll make sure it works anyway.
    """
    a = list(dem_rast.affine)
    assert a == [3.001033817607919, 0.0, 298084.90273837483, 0.0, -3.000297749750989, 130585.16954964717, 0.0, 0.0, 1.0]

def test_raster_shape(dem_rast):
    """Make sure that the dimensions of the raster match our test raster"""
    width = dem_rast.width
    height = dem_rast.height

    assert width == 1147 and height == 974
