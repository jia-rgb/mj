# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:48:57 2020

@author: jejia
"""
#%%
# get data

import pandas as pd

#matplotlib inline
df=pd.read_csv(r'C:\Users\jejia\Desktop\DataScience\pilot19 jun- dec.csv')
df3 = df[['CrewMemberId','InstructorGrade','CompetencyGrade']]

df3.sort_values(by='CrewMemberId')


#%%  
# how many NAN
df3.isnull().sum()
print

#delete rows that have NAN
df4=df3.dropna(subset=['InstructorGrade','CompetencyGrade'],how='any')
print('size after delete nan',df4.shape)

# transfer "conpetency grade" to integer
df4['CompetencyGrade'] = pd.to_numeric(df4['CompetencyGrade'], errors='coerce')

#calculate grouped mean, save in df_5col
df5 = df4[['CrewMemberId','InstructorGrade']].groupby('CrewMemberId').mean()
df6 = df4[['CrewMemberId','CompetencyGrade']].groupby('CrewMemberId').mean()

#combine df5 and df6
df7 = pd.merge(df5,df6, on = 'CrewMemberId')

#%%

# 散点图
import matplotlib.pyplot as plt

x = df7['InstructorGrade']
y = df7['CompetencyGrade']
plt.title('pilot training performance')
p = plt.scatter(x,y,color='blue')

plt.show()


#%%

#kmean
from sklearn.cluster import KMeans
import numpy as np

#e=np.append(df7,axis=0) 
X = np.array(df7)

kmeans = KMeans(n_clusters=4, random_state=0).fit(X)
kmeans.labels_


kmeans.predict([[2,0],[3,3]])

kmeans.cluster_centers_


#print(labels)
from matplotlib import pyplot as plt
label_pred = kmeans.labels_

mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
#'or' means circle - red
color = 0
j = 0 
for i in label_pred:
    plt.plot([X[j:j+1,0]], [X[j:j+1,1]], mark[i], markersize = 5)
    j +=1
plt.show()



#%%

print(df['FlaggedBehaviorIndicatorName'].unique()) 
