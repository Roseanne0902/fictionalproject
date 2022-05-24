
# coding: utf-8

# In[1]:


import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose #library for time series analysis


# In[2]:


df = pd.read_csv("dataset_2017_2020.csv")


# In[3]:


df.columns


# In[4]:


df['transaction_date'] = df.transaction_date.str[:10] #avoid time in date
df['t_date'] = pd.to_datetime(df.transaction_date) #convert to date format
df['t_date'] = df.t_date + pd.offsets.MonthBegin(-1) #send dates to first day of the month


# In[5]:


df.head()


# In[6]:


cheese = df[df.commodity.str.lower().str.contains('cheese')].copy()
cheese.head()


# In[7]:


#Just keep a simple dataframe that will contain the time series.
cheese_ts = cheese.groupby(['t_date']).agg(total_revenue=('price', sum))
cheese_ts.head(36)


# In[8]:


cheese_ts.plot();


# In[9]:


# Calculating the 6month Moving Average 
cheese_tail = cheese_ts.rolling(window=6) 
moving_avg = cheese_tail.mean()
print(moving_avg.head(41))
#NaN means not a number and is a numeric data type used to represent any value that is undefined or unpresentable


# In[10]:


fig, ax = plt.subplots(1,1)
cheese_ts.plot(ax=ax);
moving_avg.plot(color = 'red', ax=ax)
plt.legend(['current','forecast'])
plt.show();


# In[ ]:




