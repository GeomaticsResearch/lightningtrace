try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Quickly contour a digital elevation model using rasterio and matplotlib',
    'author': 'Michael Ewald / GeomaticsResearch LLC',
    'url': 'https://github.com/GeomaticsResearch/lightningtrace',
    'download_url': 'https://github.com/GeomaticsResearch/lightningtrace/archive/0.2.0.tar.gz',
    'author_email': 'mewald@geomaticsresearch.com',
    'version': '0.2.0',
    'install_requires': ['rasterio', 'fiona', 'matplotlib', 'shapely'],
    'extras_require': {
        'examples': ['geopandas',],
        'tests': ['pytest',]
    },
    'packages': ['lightningtrace'],
    'scripts': [],
    'name': 'lightningtrace',
    'classifiers': [
                      'Development Status :: 3 - Alpha',
                      'License :: OSI Approved :: MIT License',
                      'Topic :: Scientific/Engineering',
                      'Topic :: Scientific/Engineering :: GIS',
                      'Topic :: Scientific/Engineering :: Visualization',
                      'Intended Audience :: Developers',
                      'Operating System :: MacOS :: MacOS X',
                      'Operating System :: Microsoft :: Windows',
                      'Operating System :: POSIX',
                      'Programming Language :: Python',
                  ],
}

setup(**config)