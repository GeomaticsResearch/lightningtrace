import pytest
import lightningtrace


@pytest.yield_fixture
def dem_rast():
    """Open the test DEM as a fixture"""
    import os.path
    import rasterio
    with rasterio.open(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data', 'dem.img'), 'r') as rast:
        yield rast


def test_world_to_pixel_transformation(dem_rast):
    """Can we convert world coordinates to pixel coordinates?"""
    pixel_coordinates = 545.4898088852788, 516.4572418773387
    world_coords = 299721.936102, 129035.644049
    res = lightningtrace.transformations.world_to_pixel_coords(dem_rast.affine, world_coords)
    assert round(res[0]-pixel_coordinates[0], 5) == 0 and round(res[1]-pixel_coordinates[1], 5) == 0


def test_pixel_to_world_transformation(dem_rast):
    """Can we convert from pixel to world coordinates?"""
    pixel_coordinates = 545.4898088852788, 516.4572418773387
    world_coords = 299721.936102, 129035.644049
    res = lightningtrace.transformations.pixel_to_world_coords(dem_rast.affine, pixel_coordinates)
    assert round(res[0] - world_coords[0], 5) == 0 and round(res[1] - world_coords[1], 5) == 0