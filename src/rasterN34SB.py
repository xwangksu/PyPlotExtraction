'''
Created on Nov 16, 2018

@author: xuwang
'''
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *
import numpy as np

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True,
    help="source raster file folder")
args = ap.parse_args()
filePath = args.srcFolder

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()
crs = QgsCoordinateReferenceSystem("EPSG:4326")

# for im in imList:
dateString = str(filePath).split('\\')[-1]
ndviIm = filePath + '\\' + dateString + '_ortho_NDVI.tif'
rnSatIm = filePath + '\\' + dateString + '_rnSat.tif'
nHueIm = filePath + '\\' + dateString + '_nHue.tif'

ndviOrthoTiffInfo = QFileInfo(ndviIm)
ndviOrthoTiffBaseName = ndviOrthoTiffInfo.baseName()
ndviOrthoTiffLayer = QgsRasterLayer(ndviIm, ndviOrthoTiffBaseName)

rnSatOrthoTiffInfo = QFileInfo(rnSatIm)
rnSatOrthoTiffBaseName = rnSatOrthoTiffInfo.baseName()
rnSatOrthoTiffLayer = QgsRasterLayer(rnSatIm, rnSatOrthoTiffBaseName)

nHueOrthoTiffInfo = QFileInfo(nHueIm)
nHueOrthoTiffBaseName = nHueOrthoTiffInfo.baseName()
nHueOrthoTiffLayer = QgsRasterLayer(nHueIm, nHueOrthoTiffBaseName)

n3Tiff = filePath + '\\' + dateString + '_n3.tif'

# Define each band within the ortho raster layer
entries = []
# Define ndvi band
ndviBand = QgsRasterCalculatorEntry()
ndviBand.ref = ndviOrthoTiffLayer.name() + '@1'
ndviBand.raster = ndviOrthoTiffLayer
ndviBand.bandNumber = 1
entries.append(ndviBand)
# Define rnSat band
rnSatBand = QgsRasterCalculatorEntry()
rnSatBand.ref = rnSatOrthoTiffLayer.name() + '@1'
rnSatBand.raster = rnSatOrthoTiffLayer
rnSatBand.bandNumber = 1
entries.append(rnSatBand)
# Define nHue band
nHueBand = QgsRasterCalculatorEntry()
nHueBand.ref = nHueOrthoTiffLayer.name() + '@1'
nHueBand.raster = nHueOrthoTiffLayer
nHueBand.bandNumber = 1
entries.append(nHueBand)

# Generate n3 Tiff
genN3 = QgsRasterCalculator(
        '( ' + ndviBand.ref + ' + ' + rnSatBand.ref + ' + ' + nHueBand.ref + ' ) / 3 ',
                                 n3Tiff, 'GTiff', ndviOrthoTiffLayer.extent(), ndviOrthoTiffLayer.width(),
                                 ndviOrthoTiffLayer.height(), entries)
genN3.processCalculation()

qgs.exitQgis()

