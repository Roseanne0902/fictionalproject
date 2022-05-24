
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import statistics 


# In[4]:


df = pd.read_csv("Customer_Calls_Categorised.csv")


# In[5]:


df.head(10) #This line will print the first N rows


# In[6]:


df.Type.nunique() #Number of unique types


# In[15]:


# Easy way to see descriptive stats by using method describe(). We have to transpose the original df first.
# Median is the 50% percentile. 
df.set_index('Type').transpose().reset_index().describe()


# In[16]:


df.set_index('Type').transpose().reset_index().describe().to_csv("describe_output.csv") #send everything to a csv


# In[10]:


df


# In[18]:


#Doing the calculations column by column
test = df.copy()
test.set_index('Type', inplace=True)
tc = test.columns
test['min'] = test[tc].min(axis=1)
test['max'] = test[tc].max(axis=1)
test['mean'] = test[tc].mean(axis=1)
test['sum'] = test[tc].sum(axis=1)
test[['min', 'max', 'mean', 'sum']]
test.head()


# In[12]:


test[['min', 'max', 'mean', 'sum']].to_csv("manual_descriptive.csv")


# In[ ]:




