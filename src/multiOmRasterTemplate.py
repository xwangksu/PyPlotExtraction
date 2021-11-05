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
    # redTiff = imFileName.replace(".tif","_R.tif")
    # greenTiff = imFileName.replace(".tif","_G.tif")
    # blueTiff = imFileName.replace(".tif","_B.tif")
    # redEdgeTiff = imFileName.replace(".tif","_RE.tif")
    # nirTiff = imFileName.replace(".tif","_NIR.tif")
    # ndviTiff = imFileName.replace(".tif","_NDVI.tif")
    # ndreTiff = imFileName.replace(".tif","_NDRE.tif")
    # gNDVITiff = imFileName.replace(".tif","_GNDVI.tif")
    ndviTiff = imFileName.replace(".tif","_NDVI_temp.tif")
    # Define each band within the ortho raster layer
    entries = []
    # Define red band
    redBand = QgsRasterCalculatorEntry()
    redBand.ref = orthoTiffLayer.name()+'@3'
    redBand.raster = orthoTiffLayer
    redBand.bandNumber = 3
    entries.append(redBand)
    # Define Nir band
    nirBand = QgsRasterCalculatorEntry()
    nirBand.ref = orthoTiffLayer.name()+'@5'
    nirBand.raster = orthoTiffLayer
    nirBand.bandNumber = 5
    entries.append(nirBand)
    # Generate NDVI template Tiff
    genNDVITemp = QgsRasterCalculator( '(( '+nirBand.ref+' - '+redBand.ref+' ) / ( '+nirBand.ref+' + '+redBand.ref+' )) > 0.5',
        ndviTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
    genNDVITemp.processCalculation()


qgs.exitQgis()