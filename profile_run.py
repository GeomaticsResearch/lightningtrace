import pandas as pd
import numpy as np
import rasterio
import cProfile
from lightningtrace.core import contour_dem, _contour_mpl_worker, _trace_mpl_contour
from lightningtrace.utils import seq
from matplotlib import _cntr as cntr


def test_func():
    dem_fp = 'data/be42124a2_fixed.img'
    bbox = (298955.40 - 1000, 128310.82 - 1000, 300842.31 + 1000, 129779.57 + 1000)

    with rasterio.open(dem_fp, 'r') as rast:  # Open the raster
        # Generate the new contour
        contours = list()
        for contour_below_elev in seq(870, 1000, 10):
            contours.extend(list(
                _contour_mpl_worker(rast, [contour_below_elev, ], band=1, bbox=bbox, logger=None)))
        return contours


def test_func_optimized():
    dem_fp = 'data/be42124a2_fixed.img'
    bbox = (298955.40 - 1000, 128310.82 - 1000, 300842.31 + 1000, 129779.57 + 1000)

    with rasterio.open(dem_fp, 'r') as rast:  # Open the raster
        band_np = rast.read(1)
        band_transposed = np.transpose(band_np)
        del band_np
        rast_a = rast.affine
        rast_x, rast_y = np.mgrid[:band_transposed.shape[0], :band_transposed.shape[1]].astype('float32')
        world_x, world_y = rast_a * (rast_x, rast_y)
        del rast_x
        del rast_y

        #rast_pd = pd.DataFrame.from_records({'X': world_x, 'Y': world_y, 'Z': band_transposed}, columns=['X', 'Y', 'Z'])
        #rast_pd_bbox = rast_pd.loc[
        #    (rast_pd['X'] >= bbox[0]) & (rast_pd['X'] <= bbox[2]) & (rast_pd['Y'] >= bbox[1]) & (rast_pd['Y'] <= bbox[3]), :]
        #c = cntr.Cntr(rast_pd_bbox['X'].values, rast_pd_bbox['Y'].values, rast_pd_bbox['Z'].values)
        c = cntr.Cntr(world_x, world_y, band_transposed)
        contours = list()
        for contour_below_elev in seq(870, 1000, 10):
            contours.append(_trace_mpl_contour(c, contour_below_elev))
        return contours

if __name__ == "__main__":
    #test_func_optimized()
    cProfile.run("test_func()", sort=1)
    cProfile.run("test_func_optimized()", sort=1)