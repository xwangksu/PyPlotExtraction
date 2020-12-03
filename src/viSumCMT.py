'''
Created on Jul 9, 2020

@author: xuwang
'''
import pandas as pd

dateOptions = ['200205', '200214', '200225']
fieldTrial = ['YTBW_96-116', 'YTBW_117-137','YTBW_138-158','YTBW_159-179','YTBW_180-200',
            'YTBW_201-221','YTBW_222-242','YTBW_243-263','YTBW_264-284',
            'YTBW_285-305','YTBW_306-311', 'EYTBW_1-18','EYTBW_19-36','EYTBW_EHT_1-18',
            'EYTBW_EHT_19-36','EYTBW_EHT_37-45','EYTHP_37-45','YTBW_1-18','YTBW_19-36',
            'YTBW_37-54','YTBW_55-72']
sourceFilePath = 'J:/2020_CIMMYT/RedEdge/csv_raw/'
viRaster = ['G','R','RE','Nir','GNDVI','NDRE','NDVI']
tPath = 'J:/2020_CIMMYT/RedEdge/csv/'
for dt in dateOptions:
    for ft in fieldTrial:
        try:
            finalFile = open(tPath+dt+'_'+ft+".csv",'wt')
            df = pd.read_csv('J:/2020_CIMMYT/RedEdge/csv_raw/'+dt+'_'+ft+'_B.csv')
            df.drop(df[(df['Plot_ID'] == 'BAJ#1-1') | (df['Plot_ID'] == 'BAJ#1-2')].index, inplace = True)
            df.drop(df[(df['Plot_ID'] == 'BORL-1') | (df['Plot_ID'] == 'BORL-2')].index, inplace = True)
            df.drop(df[(df['Plot_ID'] == 'BORLAUG-1') | (df['Plot_ID'] == 'BORLAUG-2')].index, inplace = True)
            df.drop(df[(df['Plot_ID'] == 'borlaug-1') | (df['Plot_ID'] == 'borlaug-2')].index, inplace = True)
            df.drop(df[(df['Plot_ID'] == 'borl-1') | (df['Plot_ID'] == 'borl-2')].index, inplace = True)
            df.drop(df[(df['Plot_ID'] == 'borLaug-1') | (df['Plot_ID'] == 'borLaug-2')].index, inplace = True)
            
            # print(df.head(20))
            for vr in viRaster:
                sFile = 'J:/2020_CIMMYT/RedEdge/csv_raw/'+dt+'_'+ft+'_'+vr+'.csv'
                df_temp = pd.read_csv(sFile)
                # df_temp.head()
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'BAJ#1-1') | (df_temp['Plot_ID'] == 'BAJ#1-2')].index, inplace = True)
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'BORL-1') | (df_temp['Plot_ID'] == 'BORL-2')].index, inplace = True)
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'BORLAUG-1') | (df_temp['Plot_ID'] == 'BORLAUG-2')].index, inplace = True)
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'borlaug-1') | (df_temp['Plot_ID'] == 'borlaug-2')].index, inplace = True)
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'borl-1') | (df_temp['Plot_ID'] == 'borl-2')].index, inplace = True)
                df_temp.drop(df_temp[(df_temp['Plot_ID'] == 'borLaug-1') | (df_temp['Plot_ID'] == 'borLaug-2')].index, inplace = True)
                
                df = df.merge(df_temp, on='Plot_ID', how='left')
                # df.head()
            df['Plot_ID']=df['Plot_ID'].str[:-2]
            df3 = df.groupby(['Plot_ID']).mean()
            df3.to_csv(finalFile, index=True)
        finally:
            finalFile.close()
