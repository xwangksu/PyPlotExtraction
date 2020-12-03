'''
Created on Oct 9, 2018

@author: xuwang
'''
# import os
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *
import os
import argparse

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()
crs = QgsCoordinateReferenceSystem("EPSG:4326")

#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFolder", required=True,
    help="source images")
#==============
# ap.add_argument("-t", "--targetFolder", required=True,
#     help="target folder")
#==============
args = ap.parse_args()
filePath = args.srcFolder
# targetPath = args.targetFolder
# Create list of all images
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the path: %d" % len(imList))

for im in imList:
# Raster layer define
    orthoTiffInfo = QFileInfo(im)
    orthoTiffBaseName = orthoTiffInfo.baseName()
    orthoTiffLayer = QgsRasterLayer(im, orthoTiffBaseName)
    if not orthoTiffLayer.isValid():
        print("Layer failed to load!")
    # Tiff saving define
    imFileName = str(im)
    ctTiff = imFileName.replace("_1.tif","_ct.tif")
    # Define each band within the ortho raster layer
    entries = []
    # Define ct band
    ctBand = QgsRasterCalculatorEntry()
    ctBand.ref = orthoTiffLayer.name()+'@6'
    ctBand.raster = orthoTiffLayer
    ctBand.bandNumber = 6
    entries.append(ctBand)
    
    # Generate red Tiff
    genRed = QgsRasterCalculator( ctBand.ref,
        ctTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
    genRed.processCalculation()

qgs.exitQgis()