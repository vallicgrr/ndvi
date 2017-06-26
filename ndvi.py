#!/usr/bin/env python

# ndvi.py red.tif nir.tif output-ndvi.tif

import numpy as np
from sys import argv
from osgeo import gdal, gdalconst

t = np.float32

red, nir = map(gdal.Open, argv[1:3])

geotiff = gdal.GetDriverByName('GTiff')
output = geotiff.CreateCopy(argv[3], red, 0)

output = geotiff.Create(
   argv[3], 
   red.RasterXSize, red.RasterYSize, 
   1, 
   gdal.GDT_UInt16)

r = red.GetRasterBand(1).ReadAsArray(0, 0, red.RasterXSize, red.RasterYSize)
n = nir.GetRasterBand(1).ReadAsArray(0, 0, nir.RasterXSize, nir.RasterYSize)

r = r.astype(t)
n = n.astype(t)

np.seterr(invalid='ignore')

ndvi = (n - r)/(n + r)
ndvi = (ndvi + 1) * (2**15 - 1)
ndvi = ndvi.astype(np.uint16)

output.GetRasterBand(1).WriteArray(ndvi)
