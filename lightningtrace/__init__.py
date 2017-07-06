import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()
import shapely
import numpy as np
from matplotlib import _cntr as cntr
import rasterio

import lightningtrace.core
import lightningtrace.transformations
import lightningtrace.utils
import lightningtrace.contour
