
# coding: utf-8

# # Task 4.2.1

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("dataset_2017_2020.csv")


# We use the method plot() to display the total revenue in the last 3 years
# This is a quick way to display the information. The graph is not interactive.
# This graph is straigthforward as transaction_date becomes one of our x-axis and total revenue is our y-axis

# In[4]:


#Groupby is a pretty simple concept. We can create a grouping of categories and apply a function to the categories. 
#The returned chart provides and overview of revenue over time to provide a bit picture overview of seasonal trends.
df.groupby(['transaction_date']).agg(total_revenue=('price', sum)).plot()


# In[5]:


df.transaction_date = pd.to_datetime(df.transaction_date) #Have to change to datetime format
df["year"] = df.transaction_date.dt.year
df.groupby(['year']).agg(total_revenue=('price', sum)).head()


# We pass to the plot method 2 parameters
# 
# 1) figsize, which receives a tuple (10,5), this tuple has the width and heigth of the plot container.
# 
# 2) title is the parameter to define the name of the plot.

# In[7]:


df.groupby(['year']).agg(total_revenue=('price', sum)).plot(figsize=(10, 5), title= "Revenue trends")


# In[8]:


df.transaction_date = pd.to_datetime(df.transaction_date) #Have to change to datetime format
df["month"] = df.transaction_date.dt.month
df.groupby(['month']).agg(total_revenue=('price', sum)).head(12)


# In[9]:


df.groupby(['month']).agg(total_revenue=('price', sum)).plot(figsize=(10, 5), title= "Revenue trends")


# In[ ]:




