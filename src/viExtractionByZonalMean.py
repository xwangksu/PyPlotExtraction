'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv
import numpy as np


dateStamp = ['20210924']

def nonZeroMean(x):
    return np.sum(x)/np.count_nonzero(x)

sPath='G:/2021_INIA/ortho/'
viRaster = ['GNDVI','NDRE','NDVI']
bandRaster = ['B','G','R','RE','Nir']
for ds in dateStamp:
    shapeFile = 'G:/2021_INIA/shapefiles/field_20210924.shp'
    for vi in viRaster:
        finalFile = open(sPath+ds+'_'+vi+".csv",'wt')
        rasterFile = sPath+ds+"_ortho_"+vi+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = 'median', add_stats={'mymean':nonZeroMean}, geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',vi))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.3f}'.format(rasterMean[i]['properties'].get('median'))
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
    for bd in bandRaster:
        finalFile = open(sPath+ds+'_'+bd+".csv",'wt')   
        rasterFile = sPath+ds+'_ortho_'+bd+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = 'median', add_stats={'mymean':nonZeroMean}, geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',bd))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.3f}'.format(float(rasterMean[i]['properties'].get('median'))/32768)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
