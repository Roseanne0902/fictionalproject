
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv('dataset_2017_2020.csv',sep=",")
df.head()


# In[17]:


df[["basket_id", "department", "age_band"]]


# In[85]:


df.groupby("transaction_date").agg(total_revenue=('price', sum)).head()


# In[41]:


df.transaction_date=pd.to_datetime(df.transaction_date)
df['year']=df.transaction_date.dt.year
df.head()


# In[86]:


df.groupby("year").agg(total_reve=('price', 'sum')).head()


# In[64]:


df[df.transaction_date.dt.month < 7].groupby(['year']).agg({'price': ['min', 'max', 'sum', 'mean']}).head()


# In[68]:


df.groupby(["brand", "year"]).agg(total_reve=('price', sum))


# In[67]:


df.groupby("brand").agg(avg_revenue=('price', 'mean'))


# In[71]:


df.groupby("commodity").agg(avg=("price",'mean'))


# In[15]:


df.groupby("commodity").agg(avg=("price",'max'))


# In[78]:


df.groupby("commodity").agg(min_value=("price",'min'))


# In[81]:


df.groupby("commodity").agg(min_value=("price",'min')).sort_values('min_value', ascending=False)


# In[3]:


# Visualization
import pandas as pd
import numpy as np


# In[4]:


df=pd.read_csv('dataset_2017_2020.csv',sep=",")
df.head()


# In[18]:


df.transaction_date=pd.to_datetime(df.transaction_date)
df['year']=df.transaction_date.dt.year
df['month']=df.transaction_date.dt.month
df['week']=df.transaction_date.dt.isocalendar().week
df.head(80)


# In[12]:


df.groupby('week').agg(total_revenue=('price',sum))


# In[25]:


df.groupby('month').agg(total_revenue=('price',sum)).sort_values('total_revenue', ascending=True)


# In[13]:


np.unique(df['loyalty'])


# In[ ]:





# In[ ]:




