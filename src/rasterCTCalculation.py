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

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()
crs = QgsCoordinateReferenceSystem("EPSG:4326")

imgSrcPath = 'F:/2019_KS_Wheat/THI_PHS_EAST/'
# orthoTiff = imgSrcPath+'ortho.tif'
# # Ortho raster layer define
# orthoTiffInfo = QFileInfo(orthoTiff)
# orthoTiffBaseName = orthoTiffInfo.baseName()
# orthoTiffLayer = QgsRasterLayer(orthoTiff, orthoTiffBaseName)
# if not orthoTiffLayer.isValid():
#     print("Layer failed to load!")
dateStamp = ['20190611','20190617','20190620','20190624','20190625','20190627','20190709','20190713']
loc='_'
for ds in dateStamp:
    orthoTiff = imgSrcPath+ds+'/ortho.tif'
    # Ortho raster layer define
    orthoTiffInfo = QFileInfo(orthoTiff)
    orthoTiffBaseName = orthoTiffInfo.baseName()
    orthoTiffLayer = QgsRasterLayer(orthoTiff, orthoTiffBaseName)
    if not orthoTiffLayer.isValid():
        print("Layer failed to load!")
    # Tiff saving define

    ctTiff = imgSrcPath+ds+'/'+ds+loc+'CT.tif'
    # Define each band within the ortho raster layer
    entries = []
    # Define CT band
    ctBand = QgsRasterCalculatorEntry()
    ctBand.ref = orthoTiffLayer.name()+'@6'
    ctBand.raster = orthoTiffLayer
    ctBand.bandNumber = 5
    entries.append(ctBand)
    # Generate ct Tiff
    genCT = QgsRasterCalculator( ctBand.ref,
        ctTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
    genCT.processCalculation()
    

qgs.exitQgis()