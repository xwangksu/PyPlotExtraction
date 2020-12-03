'''
Created on Jul 9, 2020

@author: xuwang
'''
import pandas as pd

dateOptions = ['20180119', '20180223', '20180302', '20180307', '20180312', '20180319']

sourceFilePath = 'F:/2018_CIMMYT_PC_M/Orthomosaic/csv_raw/'
viRaster = ['G','R','RE','Nir','GNDVI','NDRE','NDVI']
tPath = 'F:/2018_CIMMYT_PC_M/CSV/'
for dt in dateOptions:
#     for ft in fieldTrial:
    try:
        finalFile = open(tPath+dt+'_VIs.csv','wt')
        df = pd.read_csv(sourceFilePath+dt+'_B.csv')            
        # print(df.head(20))
        for vr in viRaster:
            sFile = sourceFilePath+dt+'_'+vr+'.csv'
            df_temp = pd.read_csv(sFile)
            # df_temp.head()
            df = df.merge(df_temp, on='Plot_ID', how='left')
            # df.head()
#             df['Plot_ID']=df['Plot_ID'].str[:-2]
#             df3 = df.groupby(['Plot_ID']).mean()
        df.to_csv(finalFile, index=False)
    finally:
        finalFile.close()
