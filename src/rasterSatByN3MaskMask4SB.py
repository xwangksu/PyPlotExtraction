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
ap.add_argument("-thresh", "--thValue", required=True,
    help="mask threshold")
args = ap.parse_args()
filePath = args.srcFolder
th = args.thValue

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()
crs = QgsCoordinateReferenceSystem("EPSG:4326")

# for im in imList:
dateString = str(filePath).split('\\')[-1]
n3Im = filePath + '\\' + dateString + '_rnSat_n3mask.tif'


n3OrthoTiffInfo = QFileInfo(n3Im)
n3OrthoTiffBaseName = n3OrthoTiffInfo.baseName()
n3OrthoTiffLayer = QgsRasterLayer(n3Im, n3OrthoTiffBaseName)

n3MaskTiff = filePath + '\\' + dateString + '_rnSat_n3mask_mask.tif'

# Define each band within the ortho raster layer
entries = []
# Define ndvi band
n3Band = QgsRasterCalculatorEntry()
n3Band.ref = n3OrthoTiffLayer.name() + '@1'
n3Band.raster = n3OrthoTiffLayer
n3Band.bandNumber = 1
entries.append(n3Band)


# Generate n3 mask Tiff
genN3Mask = QgsRasterCalculator(
        n3Band.ref + ' >= ' + th,
                                 n3MaskTiff, 'GTiff', n3OrthoTiffLayer.extent(), n3OrthoTiffLayer.width(),
                                 n3OrthoTiffLayer.height(), entries)
genN3Mask.processCalculation()

qgs.exitQgis()

