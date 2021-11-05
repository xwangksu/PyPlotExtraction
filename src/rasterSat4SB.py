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

exten = '_sat.tif'
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

    # orthoTiffLayer.renderer().setRedBand(3)
    # orthoTiffLayer.renderer().setGreenBand(2)
    # orthoTiffLayer.renderer().setBlueBand(1)
    satTiff = imFileName.replace('_Sat.tif', '_rnSat.tif')

    renderer = orthoTiffLayer.renderer()
    provider = orthoTiffLayer.dataProvider()
    
    layer_extent = orthoTiffLayer.extent()
    uses_band = renderer.usesBands()
    # print(uses_band)
    
    satType = renderer.dataType(uses_band[0])
    satStats = provider.bandStatistics(uses_band[0], QgsRasterBandStats.All, layer_extent, 0)
    
    # greenType = renderer.dataType(uses_band[1])
    # greenStats = provider.bandStatistics(uses_band[1], QgsRasterBandStats.All, layer_extent, 0)
    #
    # blueType = renderer.dataType(uses_band[2])
    # blueStats = provider.bandStatistics(uses_band[2], QgsRasterBandStats.All, layer_extent, 0)
    
    # pixMin = np.max([redStats.minimumValue, greenStats.minimumValue, blueStats.minimumValue])
    # pixMax = np.min([redStats.maximumValue, greenStats.maximumValue, blueStats.maximumValue])
    satMin = satStats.minimumValue
    satMax = satStats.maximumValue
    print(satMin)
    print(satMax)

    # Define each band within the ortho raster layer
    entries = []
    # Define red band
    satBand = QgsRasterCalculatorEntry()
    satBand.ref = orthoTiffLayer.name() + '@1'
    satBand.raster = orthoTiffLayer
    satBand.bandNumber = 1
    entries.append(satBand)
    # Generate sat Reverse Tiff
    genSat = QgsRasterCalculator(
        '( 255 - ' + satBand.ref + ' ) / 255 ',
                                 satTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(),
                                 orthoTiffLayer.height(), entries)
    genSat.processCalculation()

qgs.exitQgis()

