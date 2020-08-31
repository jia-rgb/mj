# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:20:47 2020

@author: jejia
"""

import pandas as pd
df=pd.read_csv(r'C:\Users\jejia\Desktop\DataScience\easyjet\data\easyJet_Pilot_Training_Data - v2.csv')



grade_ONLY_0=df[['UniqueID_candidate','form_title','base','fleet','crew_rank','total_hours','hours_on_type','stage_of_training','type_of_training','Date','UniqueID_trainer',
                 'apk_grade','com_grade','fpa_grade','fpm_grade','kno_grade','ltw_grade','psd_grade','saw_grade','wlm_grade']].melt(['UniqueID_candidate','form_title','base',
                                                                                         'fleet','crew_rank','total_hours','hours_on_type','stage_of_training','type_of_training',
                                                                                         'Date','UniqueID_trainer'], var_name='Competency', value_name = 'grade')
grade_ONLY = grade_ONLY_0.dropna(subset=['grade'],how='any') 
grade_ONLY = grade_ONLY.sort_values(by = ['UniqueID_candidate'])
 

#grade_number = grade_ONLY['grade'].str.split('.',expand=True)
grade_ONLY['grade1'] = grade_ONLY['grade'].map(lambda x:x.split('.')[0])
grade_ONLY['grade_level_name'] = grade_ONLY['grade'].map(lambda x:x.split('.')[1])
grade_ONLY['hours_on_type_int'] = grade_ONLY.hours_on_type.replace(['Less than 500','500 to 999',
                                                                '1000 to 1999','2000 to 2999',
                                                                '3000 to 4999', 'Over 5000'],
                                                               [500, 999, 1999,2999,4999, 5001])
grade_ONLY['hours_on_type_int'] = pd.to_numeric(grade_ONLY['hours_on_type_int'])
T2_check = grade_ONLY[(grade_ONLY["form_title"] == 'T2 - Proficiency Check')&
                      (grade_ONLY["stage_of_training"] == 'Recurrent')]
#%%#grade_ONLY['grade1'] = grade_ONLY['grade1'].astype('float', copy=False)
grade_ONLY1 = T2_check[['grade1','UniqueID_candidate','hours_on_type_int','crew_rank']]
people0 = list(grade_ONLY['UniqueID_candidate'].unique()) 
#%% differentiate FO and CP
grade_ONLY1['grade1'] = pd.to_numeric(grade_ONLY1['grade1'])


data_CP = grade_ONLY1[grade_ONLY1['crew_rank']=='CP'] 


data_normal_CP = data_CP.groupby('UniqueID_candidate').mean().reset_index()

#%%
 
# take the data needed for the clustering to data.columns
 
fColumns=['grade1','hours_on_type_int']
 
# standardize by 0-1
 

CP_cluster=data_normal_CP[fColumns]
data = CP_cluster
 
data[fColumns]=round(
        (data[fColumns]-data[fColumns].min())/(data[fColumns].max()-data[fColumns].min()),
        5)
 
# import hierarchical clustering 
from scipy.cluster.hierarchy import linkage,dendrogram
 
Z=linkage(data[fColumns],method='ward',metric='euclidean') #p clustering plot
 
P=dendrogram(Z,0) # draw chart tree
 
'''#只展示12个数据
P1=dendrogram(Z,
        truncate_mode='lastp',
        p=12,
        leaf_font_size=12.
        )
'''
#%%
# import from sklearn the hierarchical clustering
import matplotlib.pyplot as plt
k = 3
from sklearn.cluster import AgglomerativeClustering 

cluster_CP = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')  
cluster_CP.fit_predict(data[fColumns]) 

#draw scatter chart
plt.figure(figsize=(10, 10))  
plt.scatter(data_normal_CP['hours_on_type_int'], data_normal_CP['grade1'], c=cluster_CP.labels_) 
plt.title('The 5 cluster CP')
plt.show()




#%%

data_normal_CP['label']=cluster_CP.labels_

CP = pd.merge(grade_ONLY, data_normal_CP[['UniqueID_candidate', 'label']], how = 'left', on=['UniqueID_candidate'])

CP['grade1'] = pd.to_numeric(CP['grade1'])
CP_1 = CP[CP['label']==1] 
CP_2 = CP[CP['label']==2] 
CP_3 = CP[CP['label']==0] 
   
#%%CP1
    
CP_11 = CP_1.groupby('grade1')['UniqueID_candidate'].count().reset_index(name = 'amount')
CP_111 = CP_1.groupby('Competency')['grade1'].mean().reset_index(name = 'grade')
CP_1111 = CP_1.groupby('UniqueID_trainer')['grade1'].mean()

CP_exp1 = CP_1[['UniqueID_candidate','total_hours']]
CP_exp1 = CP_exp1.drop_duplicates()
CP_exp_1 = CP_exp1[['UniqueID_candidate','total_hours']].groupby('total_hours').count()

CP_111P=CP_11[(CP_11['grade1'] ==1)|(CP_11['grade1'] ==2)]
#sum
CP_111P['amount'].sum()/CP_11['amount'].sum()



data_CP = grade_ONLY1[grade_ONLY1['crew_rank']=='FO'] 
data_FO = grade_ONLY1[grade_ONLY1['crew_rank']=='FO'] 
people_CP = list(data_CP['UniqueID_candidate'].unique()) 
people_FO = list(data_FO['UniqueID_candidate'].unique())
people_CP_1 = list(CP_1['UniqueID_candidate'].unique())
people_CP_2 = list(CP_2['UniqueID_candidate'].unique())
people_CP_3 = list(CP_3['UniqueID_candidate'].unique())
#%%CP1
    
CP_22 = CP_2.groupby('grade1')['UniqueID_candidate'].count().reset_index(name = 'amount')
CP_222 = CP_2.groupby('Competency')['grade1'].mean().reset_index(name = 'grade')
CP_2222 = CP_2.groupby('UniqueID_trainer')['grade1'].mean().reset_index(name = 'grade')

CP_exp2 = CP_2[['UniqueID_candidate','total_hours']]
CP_exp2 = CP_exp2.drop_duplicates()
CP_exp_2 = CP_exp2[['UniqueID_candidate','total_hours']].groupby('total_hours').count()
#%%
CP_222P=CP_22[(CP_22['grade1'] ==1)|(CP_22['grade1'] ==2)]
#sum
CP_222P['amount'].sum()/CP_22['amount'].sum()

#%%

CP_33 = CP_3.groupby('grade1')['UniqueID_candidate'].count().reset_index(name = 'amount')
CP_333 = CP_3.groupby('Competency')['grade1'].mean().reset_index(name = 'grade')
CP_3333 = CP_3.groupby('UniqueID_trainer')['grade1'].mean().reset_index(name = 'grade')
#%%
CP_33P=CP_33[(CP_33['grade1'] ==1)|(CP_33['grade1'] ==2)]
#sum
CP_33P['amount'].sum()/CP_33['amount'].sum()
    
CP_exp3 = CP_3[['UniqueID_candidate','total_hours']]
CP_exp3 = CP_exp3.drop_duplicates()
CP_exp_3 = CP_exp3[['UniqueID_candidate','total_hours']].groupby('total_hours').count()
    
#%%
data_normal_CP.to_excel(r'C:\Users\jejia\Desktop\DataScience\easyjet\dashboard\CP_cluster2.xlsx') 
    