'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv

dateStamp = ['20190611','20190617','20190620','20190624','20190625','20190627','20190709','20190713']

sPath='F:/2019_KS_Wheat/THI_PHS_EAST/'
ctRaster = ['CT']
for ds in dateStamp:
    # rasterPath = sPath+ds+"/"
    shapeFile = sPath+'shapefiles/2019_THI_PHS_east_fieldmap_shk.shp'
    for vi in ctRaster:
        finalFile = open(sPath+ds+'_'+vi+".csv",'wt')   
        rasterFile = sPath+ds+'/'+ds+'_'+vi+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "mean", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',vi))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID')#.split("$")[0]
                value = '{0:.2f}'.format((float)(rasterMean[i]['properties'].get('mean'))*0.01-273.15)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()

