try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Quickly contour a digital elevation model using rasterio and matplotlib',
    'author': 'Michael Ewald / GeomaticsResearch LLC',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'mewald@geomaticsresearch.com',
    'version': '0.1',
    'install_requires': ['pytest', 'rasterio', 'fiona', 'matplotlib', 'shapely'],
    'packages': ['lightningtrace'],
    'scripts': [],
    'name': 'lightningtrace'
}

setup(**config)