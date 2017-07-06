from setuptools import setup, find_packages
setup(
    name='lightningtrace',
    description='Quickly contour a digital elevation model using rasterio and matplotlib',
    author='Michael Ewald / GeomaticsResearch LLC',
    author_email='mewald@geomaticsresearch.com',
    url='https://github.com/GeomaticsResearch/lightningtrace',
    version='0.2.3',
    install_requires=[
        'rasterio', 'fiona', 'matplotlib', 'shapely'],
    license='MIT',
    packages=find_packages(),
    classifiers=[
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
)
