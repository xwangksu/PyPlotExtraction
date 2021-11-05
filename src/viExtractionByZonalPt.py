'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv


dateStamp = ['20200409','20200411','20200423','20200503','20200508','20200519','20200523','20200605','20200611']


sPath='E:/xuwang/2020_KS_Wheat/ASH_SPAM/ortho/'
viRaster = ['GNDVI','NDRE','NDVI']
bandRaster = ['B','G','R','RE','Nir']
for ds in dateStamp:
    shapeFile = 'E:/xuwang/2020_KS_Wheat/ASH_SPAM/shapefiles/2020_ASH_SPAM_field_raw.shp'
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
                value = '{0:.3f}'.format(float(rasterMean[i]['properties'].get('median'))/32768)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
