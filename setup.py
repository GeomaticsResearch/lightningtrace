try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Quickly contour a digital elevation model using rasterio and matplotlib',
    'author': 'Michael Ewald / GeomaticsResearch LLC',
    'url': 'https://github.com/GeomaticsResearch/lightningtrace',
    'download_url': 'Where to download it.',
    'author_email': 'mewald@geomaticsresearch.com',
    'version': '0.1.1',
    'install_requires': ['pytest', 'rasterio', 'fiona', 'matplotlib', 'shapely'],
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