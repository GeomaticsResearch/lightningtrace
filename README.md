# lightningtrace
Quickly contour a digital elevation model (DEM) using rasterio and matplotlib.

## Install
Just use pip.
`pip install lightningtrace`

## Create a Conda environment
`conda create -y -n lightningtrace rasterio shapely matplotlib numpy geopandas pytest`

## Example
The following example generates contours from the DEM at specified elevations. The `extract_contours()` function is a generator that yields GeoJSON features.
```python
import rasterio
import geopandas as gp
import lightningtrace


with rasterio.open('data/dem.img', 'r') as rast:
    # Generate the contours
    contours_to_create = [1080, 1070, 1060, 1050, 1040, 1030, 1020, 1010]
    contours = lightningtrace.contour.extract_contours(rast.read(1), rast.affine, contours_to_create)

    # Create a Geopandas DataFrame from our contours
    df = gp.GeoDataFrame.from_features(contours, rast.crs)
    print(df.head())
    df.to_file('contours.shp')
```

The library also has a few utility functions that make subsetting the raster easier and provide easy transformations between world and pixel coordinates. The result is a numpy array of (column, row) for each of the input coordinates.
```python
import rasterio
from lightningtrace.transformations import world_to_pixel_coords

with rasterio.open('data/dem.img', 'r') as rast:
  print(world_to_pixel_coords(rast.transform, [(299721.936102, 129035.644049),]))
  # returns [(545.4898088852788, 516.4572418773387),]
```

See the `examples` folder for more information.

## License
MIT

## Author
Michael Ewald, https://GeomaticsResearch.com
