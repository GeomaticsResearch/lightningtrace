import lightningtrace
import os.path
import rasterio
import geopandas as gp

# Open the raster
with rasterio.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dem.img'), 'r') as rast:
    # Subset to only a portion of the raster given by a bounding box.
    subset = lightningtrace.utils.subset_raster(rast, 1, bbox=(299000, 128000, 300000, 129300))

    # Generate the contours
    contours_to_create = [1080, 1070, 1060, 1050, 1040, 1030, 1020, 1010]
    contours = lightningtrace.contour.extract_contours(subset['array'], subset['affine'], contours_to_create)

    # Create a Geopandas DataFrame from our contours
    df = gp.GeoDataFrame.from_features(contours, rast.crs)
    print df.head()
    df.to_file('contours.shp')


