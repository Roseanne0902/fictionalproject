
# coding: utf-8

# # Task 3.3.3

# In[1]:


import pandas as pd
pd.__version__


# In[2]:


# This command will open the dataset
df = pd.read_csv("dataset_2017_2020.csv")
df.head(4) #This line will print the first N rows


# Next we only display basket_id, age_band and department. Note that you need to use double [] brackets

# In[3]:


df[['basket_id', 'age_band', 'department']]


# Let's say we wanted to know the revenue from SuperFoodsMax from each day?
# Similar to SQL, we group by the transaction date, we sum all values through the column price, and we call it total_revenue.
# It is probably a large number of days/months so we only keep the first days as an example

# In[4]:


# We use aggregate values to total the revenue for each day
df.groupby(['transaction_date']).agg(total_revenue=('price', sum)).head()


# What is the revenue in the past years?
# We need to change the transaction_date to the datetime, then we will create another column in the dataframe called "year".
# See that now the dataframe has a new column.

# In[5]:


df.transaction_date = pd.to_datetime(df.transaction_date) #Note we have to change to datetime format
df["year"] = df.transaction_date.dt.year
df.head()


# In[6]:


# Here we get the total revenue per year. Can you see trends?
df.groupby(['year']).agg(total_revenue=('price', sum))


# In[6]:


# you can also filter out by only sales until June every year so the comparison is fair
# this way to aggregate data is an old way but still supported
# one way to partition lines is splitting by calls to methods (.)
df[df.transaction_date.dt.month < 7]     .groupby(['year'])     .agg({'price': ['min', 'max', 'mean', 'sum']})
# turns out the author of the dataset predicted COVID, less sales!


# In[8]:


# Here sales are grouped by brand sales per year. What are the trends?
df.groupby(['brand', 'year']).agg(total_revenue=('price', sum))


# To calculate the average revenue in the past years we use the function "mean". What is the avg revenue in the past years for each brand type? Can you write a statement to calculate that?
# 

# In[7]:


# below code is possible because we're only grouping by one column; many columns require to be passed on as a list
df.groupby('brand').agg(avg_revenue=('price', "mean"))


# What is the price of the most expensive product in each commodity?

# In[10]:


df.groupby(['commodity'])[['price']].max()
# modern way to do it
df.groupby('commodity').agg(max_price=('price', 'max'))


# In[8]:


#What is the price of the cheapest product in each commodity?
#Try in the code cell below
df.groupby("commodity").agg(avg=("price",'min'))


# In[ ]:


#Use this code cell


# In[14]:


# There are some keywords (min, max, sum) that are Python default methods so they don't need quotation marks
# These functions are good to explore
df.groupby(['commodity']).agg(min_price=('price', 'min')).sort_values('min_price', ascending=False)

