
# coding: utf-8

# # Task 4.3.4

# In[1]:


#In this task you will just be running code to find results.


# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("dataset_2017_2020.csv")


# In[3]:


#Example 1
#Find the total revenue for the last four years. Note 2020 data ends June 30.
df.transaction_date = pd.to_datetime(df.transaction_date) #Have to change to datetime format
df["year"] = df.transaction_date.dt.year
tmp = df.groupby(['year']).agg(total_revenue=('price', sum)).reset_index()
tmp.head()


# In[4]:


#Plot the total revenue per year
plt.bar(tmp.year, tmp.total_revenue);


# # Unique products

# In[5]:


#Example 2
#Find the unique number of products in each department
df.groupby('department').agg(unique_products=('product_id', pd.Series.nunique))


# In[7]:


#Output results to a CSV file
df.groupby(['department','product_id']).agg(total_revenue=('price', sum)).to_csv('unique_products_revenue.csv')


# In[8]:


#Output results to a CSV file and include the commodity name
df.groupby(['department', 'product_id' ,'commodity']).agg(total_revenue=('price', sum)).to_csv('unique_commodities_revenue.csv')


# # Top selling departments

# In[11]:


#Example 3
#Find the top 5 selling departments by revenue. There is a total of 11 departments
top_5d = df.groupby(['department']).agg(total_revenue=('price',sum))     .sort_values('total_revenue', ascending = False).reset_index().head(5)


# In[12]:


top_5d


# In[13]:


#Eample 4
# Get the top selling commodities in the top 5 departments
tmp = df[df.department.isin(top_5d.department.unique())].groupby(['department', 'commodity']).agg(total_revenue=('price', sum)).reset_index()
top_5c = pd.concat(
    [tmp[tmp.department == hh] \
         .sort_values('total_revenue', ascending=False) \
     .head(5) for hh in top_5d.department.unique()]).reset_index(drop=True)
top_5c


# In[15]:


#Example 5
# Count the number of unique customers of these 5 departments and commodities by their loyalty type
# Note the number of rows, we **must** get 75 (5 departments * 5 commodities * 3 loyalty types = 75)
# this will not work as there are commodities appearing in more than one department
# (e.g. Salad appearing in Salad Bar department) which will add that department
df[df.commodity.isin(top_5c.commodity)]     .groupby(['department', 'commodity', 'loyalty'])     .agg(customer_count=('customer_id', pd.Series.nunique))


# In[13]:


#Example 6
# We could only consider expected departments and commodities
# However, this won't work either because of the same reason (e.g. Meat - Other appears in both Meat and Groceries depts)
df[(df.department.isin(top_5d.department)) & (df.commodity.isin(top_5c.commodity))]     .groupby(['department', 'commodity', 'loyalty'])     .agg(customer_count=('customer_id', pd.Series.nunique))     .head(50)


# In[18]:


# To solve this, we need to merge the original table with the `top_5c` departments and commodities
# This will act as a SQL join as it will exclude commodities in an unexpected department
# i.e. a commodity must be from only one of the top 5 departments
# row count tells us we're right!
top_loyalty = df     .merge(top_5c[['department', 'commodity']], on=['department', 'commodity'], how='inner')     .groupby(['department', 'commodity', 'loyalty'])     .agg(customer_count=('customer_id', pd.Series.nunique))


# In[17]:


#to see the complete output, see the CSV file in 4.3.4 in Canvas
top_loyalty.to_csv('top_loyalty_split.csv')


# In[16]:


#Example 7
# Get the top selling commodities in the top 5 departments for each age_band
tmp = df[df.department.isin(top_5d.department.unique())].groupby(['department', 'commodity', 'age_band']).agg(total_revenue=('price', sum)).reset_index()
top_5c = pd.concat(
    [tmp[tmp.department == hh] \
         .sort_values('total_revenue', ascending=False) \
     .head(5) for hh in top_5d.department.unique()]).reset_index(drop=True)
top_5c


# In[17]:


# We could only consider expected departments and commodities
# However, this won't work either because of the same reason (e.g. Meat - Other appears in both Meat and Groceries depts)
df[(df.department.isin(top_5d.department)) & (df.commodity.isin(top_5c.commodity))]     .groupby(['department', 'commodity', 'age_band'])     .agg(customer_count=('customer_id', pd.Series.nunique))     .head(50)


# In[18]:


# To solve this, we need to merge the original table with the `top_5c` departments and commodities
# This will act as a SQL join as it will exclude commodities in an unexpected department
# i.e. a commodity must be from only one of the top 5 departments
# row count tells us we're right!
top_age_band = df     .merge(top_5c[['department', 'commodity']], on=['department', 'commodity'], how='inner')     .groupby(['department', 'commodity', 'age_band'])     .agg(customer_count=('customer_id', pd.Series.nunique))


# In[19]:


#to see the complete output, see the CSV file in 4.3.4 in Canvas
top_age_band.to_csv('top_age_band_split.csv')


# In[ ]:




