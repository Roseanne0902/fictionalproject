
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.graph_objects as go


# In[2]:


df = pd.read_csv('dataset_2017_2020.csv')


# In[3]:


#Use this code to see the full contents of a dataframe. Currently returns are limited to 10 rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 0)


# In[4]:


# Example 1
# how much is spent on beef every year?
beef = df[df.commodity == 'Beef'].copy()
beef.transaction_date = pd.to_datetime(beef.transaction_date, format='%Y-%m-%d')
beef['year'] = beef.transaction_date.dt.year
beef.groupby('year').agg(total_revenue=('price', sum)).plot();


# In[5]:


# Example 2 - Create a Scatter plot from Beef revenue
tmp_beef = beef.groupby('year').agg(total_revenue=('price', sum)).reset_index()
data_beef = go.Scatter(x=tmp_beef.year, y=tmp_beef.total_revenue)
    
go.Figure(
    data=data_beef,
    layout = go.Layout(
        title ='Beef consumption trends',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')  




# In[7]:


# Example 3
# how much is spent on meat every year? Note that meat contains a number of products listed here in a string from the commodities column
meat = df[df.commodity.str.lower().str.contains('meat|beef|chicken|seafood|pork')].copy()
meat.transaction_date = pd.to_datetime(meat.transaction_date, format='%Y-%m-%d')
meat['year'] = meat.transaction_date.dt.year
meat['month'] = meat.transaction_date.dt.month
meat.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[7]:


#Example 4
# What are the most popular Commodities of baskets that did not include beef.
beef_haters = df[~df.basket_id.isin(df[df.commodity == 'Beef'].basket_id.unique())]
beef_haters     .groupby('commodity').agg(total_revenue=('price', 'sum')).sort_values('total_revenue', ascending=False).head(10)


# In[9]:


# Attempt1
# Amend code from Example 1a
# how much is spent on cheese every year?

cheese = df[df.commodity == 'Cheese'].copy()
cheese.transaction_date = pd.to_datetime(cheese.transaction_date, format='%Y-%m-%d')
cheese['year'] = cheese.transaction_date.dt.year
cheese.groupby('year').agg(total_revenue=('price', sum)).plot();


# In[10]:


# Attempt 2
# Use the code in Example 1b - Create a Scatter plot from Cheese revenue
# Now plot how much is spent on cheese every year?
tmp_cheese = cheese.groupby('year').agg(total_revenue=('price', sum)).reset_index()
data_cheese = go.Scatter(x=tmp_cheese.year, y=tmp_cheese.total_revenue)
    
go.Figure(
    data=data_cheese,
    layout = go.Layout(
        title ='cheese consumption trends',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')  


# In[22]:


#Attempt 3 - Use the code in Example 1d and return 30 rows by adjusting .head(30)
# What are the most most popular Commodities of baskets that did not include cheese - Hint Change ascending to false
beef_lovers = df[~df.basket_id.isin(df[df.commodity == 'Beef'].basket_id.unique())]
beef_lovers     .groupby('commodity').agg(total_revenue=('price', 'sum')).sort_values('total_revenue', ascending=False
                                                                         ).head(30)


# In[11]:


#Example 5
# Most popular commodities of baskets that include cheese
cheeseheads = df[df.basket_id.isin(df[df.commodity == 'Cheese'].basket_id.unique())]
cheeseheads     .groupby('commodity').agg(total_revenue=('price', 'sum')).sort_values('total_revenue', ascending=False).head(10)


# In[12]:


#Attempt 4
#From Example 3
# how much is spent on dairy every year? Dairy includes Cheese, Yoghurt, Butter and Fluid Milk products
dairy = df[df.commodity.str.lower().str.contains('cheese|yoghurt|butter|fluid milk proucts')].copy()
dairy.transaction_date = pd.to_datetime(dairy.transaction_date, format='%Y-%m-%d')
dairy['year'] = dairy.transaction_date.dt.year
dairy['month'] = dairy.transaction_date.dt.month
dairy.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[13]:


#Attempt 5
#From Example 5 - Hint change ascending to True
# Most popular Commodities of baskets that did not include cheese.
dairy_haters = df[~df.basket_id.isin(df[df.commodity == 'Cheese'].basket_id.unique())]
dairy_haters     .groupby('commodity').agg(total_revenue=('price', 'sum')).sort_values('total_revenue', ascending=True).head(10)


# In[14]:


#Attempt 6
#From Example 3
# how much is spent on smallgoods every year? Smallgoods includes lunch meat, dinner sausage, bacon, deli meats
smallgoods = df[df.commodity.str.lower().str.contains('lunch meat|dinner sausage|bacon|deli meats')].copy()
smallgoods.transaction_date = pd.to_datetime(smallgoods.transaction_date, format='%Y-%m-%d')
smallgoods['year'] = smallgoods.transaction_date.dt.year
smallgoods['month'] = smallgoods.transaction_date.dt.month
smallgoods.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[15]:


#Attempt 7
#From Example 3
# how much is spent on vegetables every year? Vegetables incldde carrots, potatoes, onions, peppers,vegetables salad, vegetables shelf stable, vegetables - all others, corn,broccoli, cauliflower.
vegetables = df[df.commodity.str.lower().str.contains('carrots|potatoes|onions|peppers|vegetables salad|vegetables - shelf stable|vegetables - all others|corn|broccoli/cauliflower')].copy()
vegetables.transaction_date = pd.to_datetime(vegetables.transaction_date, format='%Y-%m-%d')
vegetables['year'] = vegetables.transaction_date.dt.year
vegetables['month'] = vegetables.transaction_date.dt.month
vegetables.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[16]:


#Use this code to see the full contents of a dataframe. Currently returns are limited to 10 rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 0)


# In[17]:


#Example 6
#Use this code to find all unique products. You will now see all avaiable rows
df.groupby('commodity').agg(number_commodities=('commodity', pd.Series.nunique))


# In[18]:


#Example 7
#This code will return the top selling commodities at SuperFoodsMax
df.groupby(['commodity']).agg(total_revenue=('price', sum)).sort_values('total_revenue', ascending=False).head(20)


# In[19]:


# Attempt 8 
# From Example 3
#Track the trends of the top 5 selling commodities over the years.
topfive = df[df.commodity.str.lower().str.contains('beef|cheese|frozen meat|deli meats')].copy()
topfive.transaction_date = pd.to_datetime(topfive.transaction_date, format='%Y-%m-%d')
topfive['year'] = topfive.transaction_date.dt.year
topfive['month'] = topfive.transaction_date.dt.month
topfive.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[20]:


# Attempt 9 
# From Example 3
# Track the trends of the top 10 selling commodities over the years.

topten = df[df.commodity.str.lower().str.contains('beef|cheese|frozen meat|deli meats|seafood-frozen|salad|lunch meat|pork|Cigarettes|Candy')].copy()
topten.transaction_date = pd.to_datetime(topten.transaction_date, format='%Y-%m-%d')
topten['year'] = topten.transaction_date.dt.year
topten['month'] = topten.transaction_date.dt.month
topten.groupby(['year', 'month']).agg(total_revenue=('price', sum)).plot(figsize=(12,5));


# In[ ]:


#[Slack] Investigate commodity types Example 1


# In[ ]:


#[Slack] Investigate commodity types Example 2

