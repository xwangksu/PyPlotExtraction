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

exten = '_dem.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the folder: %d" % len(imList))

for im in imList:
    orthoTiffInfo = QFileInfo(im)
    orthoTiffBaseName = orthoTiffInfo.baseName()
    orthoTiffLayer = QgsRasterLayer(im, orthoTiffBaseName)

    # Tiff saving define
    imFileName = str(im)

    demTiff = imFileName.replace('.tif', '_Norm.tif')

    renderer = orthoTiffLayer.renderer()
    provider = orthoTiffLayer.dataProvider()
    
    layer_extent = orthoTiffLayer.extent()
    uses_band = renderer.usesBands()
    # print(uses_band)
    
    demType = renderer.dataType(uses_band[0])
    demStats = provider.bandStatistics(uses_band[0], QgsRasterBandStats.All, layer_extent, 0)

    # pixMin = np.max([redStats.minimumValue, greenStats.minimumValue, blueStats.minimumValue])
    # pixMax = np.min([redStats.maximumValue, greenStats.maximumValue, blueStats.maximumValue])
    demMin = demStats.minimumValue
    demMax = demStats.maximumValue
    print(demMin)
    print(demMax)
    min_r = demMin + 0.01 * (demMax - demMin)
    max_r = demMax - 0.01 * (demMax - demMin)
    range = max_r - min_r

    # Define each band within the ortho raster layer
    entries = []
    # Define red band
    demBand = QgsRasterCalculatorEntry()
    demBand.ref = orthoTiffLayer.name() + '@1'
    demBand.raster = orthoTiffLayer
    demBand.bandNumber = 1
    entries.append(demBand)
    # Generate sat Reverse Tiff
    genDem = QgsRasterCalculator(
        '( ' + demBand.ref + ' - ' + str(min_r) + ' ) / ' + str(range),
                                 demTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(),
                                 orthoTiffLayer.height(), entries)
    genDem.processCalculation()

qgs.exitQgis()

