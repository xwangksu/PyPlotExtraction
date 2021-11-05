'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv


ds = '20200225'
fieldTrial = ['200225_YTBW_96-116','200225_YTBW_117-137','200225_YTBW_138-158','200225_YTBW_159-179','200225_YTBW_180-200','200225_YTBW_201-221','200225_YTBW_222-242','200225_YTBW_243-263','200225_YTBW_264-284','200225_YTBW_285-305','200225_YTBW_306-311']
sPath='J:/2020_CIMMYT/RedEdge/ortho/'
tPath = 'J:/2020_CIMMYT/RedEdge/csv/'
viRaster = ['GNDVI','NDRE','NDVI']
bandRaster = ['B','G','R','RE','Nir']
for ft in fieldTrial:
    shapeFile = 'J:/2020_CIMMYT/RedEdge/shapefiles/'+ft+'_shk.shp'
    for vi in viRaster:
        finalFile = open(tPath+ft+'_'+vi+".csv",'wt')   
        rasterFile = sPath+ds+'_2_ortho_'+vi+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "mean", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',vi))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.3f}'.format(rasterMean[i]['properties'].get('mean'))
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
    for bd in bandRaster:
        finalFile = open(tPath+ft+'_'+bd+".csv",'wt')   
        rasterFile = sPath+ds+'_2_ortho_'+bd+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "mean", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',bd))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.3f}'.format(float(rasterMean[i]['properties'].get('mean'))/32768)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
