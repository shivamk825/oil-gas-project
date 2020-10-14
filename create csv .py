#!/usr/bin/env python
# coding: utf-8

# In[14]:


import csv
import pandas as pd

df = pd.DataFrame()
idx = 0
new_col = ['Range Resources Corp.','occidental petroleum','Talos Energy Inc.','Chevron Corporation ','Apache Corp', 'Cabot Oil & Gas Corp.', 'EOG Resources', 'Hess Corp.', 'Marathon Oil Corp', 'Murphy Oil Corporation',  'Occidental Petroleum Corp.', 'Southwestern Energy Co.', 'EP Energy', 'Oasis Petroleum  Inc.','SILVERBOW RESOURCES','SM Energy','Concho Resources Inc.','Noble Energy Inc.'] # can be a list, a Series, an array or a scalar   
df.insert(loc=idx, column='Company', value=new_col)
df


# In[ ]:





# In[73]:





# In[15]:


df


# In[ ]:





# In[16]:


df['Enterprisevalue']=""
df['Ebitda']=""
df['Employees']=""
df['Revenue(ttm)']=""
df['Marketcap']=""


# In[17]:


df


# In[18]:


idx = 6
new_column = ['RRC','OXY','TALO','CVX','APA', 'COG', 'EOG', 'HES', 'MRO', 'MRO',  'OXY', 'SWN', 'EPSN', 'OAS','SBOW','SM','CXO','NBL.MX'] # can be a list, a Series, an array or a scalar   
df.insert(loc=idx, column='compsymbol', value=new_column)
df


# In[19]:


df.to_csv(r'C:/Users/91855/Desktop/oil and gas/oil.csv')


# In[ ]:





# In[ ]:





# In[ ]:




