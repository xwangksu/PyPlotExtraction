'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv


dateStamp = ['20180119', '20180223', '20180302', '20180307', '20180312', '20180319']


sPath='F:/2018_CIMMYT_PC_M/Orthomosaic/'
viRaster = ['GNDVI','NDRE','NDVI']
bandRaster = ['B','G','R','RE','Nir']
for ds in dateStamp:
    shapeFile = 'G:/2018_PC_Mg/shapefiles/'+ds+'_field.shp'
    for vi in viRaster:
        finalFile = open(sPath+ds+'_'+vi+".csv",'wt')   
        rasterFile = sPath+ds+'_ortho_'+vi+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "median", geojson_out=True)
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
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "median", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',bd))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.4f}'.format(float(rasterMean[i]['properties'].get('median'))/65536)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
