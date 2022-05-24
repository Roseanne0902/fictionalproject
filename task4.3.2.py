
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.graph_objects as go


# In[2]:


df = pd.read_csv('dataset_2017_2020.csv')


# In[7]:


#Example 1
#To get the bottom 10 selling commodities, change ascending = True
df.groupby(['commodity']).agg(total_revenue=('price',sum))     .sort_values('total_revenue', ascending = True).head(10)


# In[4]:


#Your attempt 1
#Amend the code in Example 1 to find the bottom 25 products


# In[5]:


#Your attempt 1 - Add your code here
#To get the bottom 25 selling commodities, change ascending = True from Example 1
#What results are you seeing?


# In[6]:


#Your attempt 2
#To get the top 25 selling commodities, change ascending = False from Example 1 and update head to 25


# In[8]:


#Example 2
#Get the top 10 commodities by revenue and chart
top_10 = df.groupby(['commodity']).agg(total_revenue=('price',sum))     .sort_values('total_revenue', ascending = False).head(10)

go.Figure(
    data = go.Bar(x=top_10.index, y=top_10['total_revenue']),
    layout = go.Layout(
        title ='Top 10 commodities',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')


# In[34]:


#Your attempt 3
#Amend the code from Example 2
#Get the top 25 commodities by revenue and chart
#Note where code has been amended


# In[8]:


#Your attempt 4 - Add your code here
#Now amend the code from Example 2 to return the top 50 commodities by revenue and chart
#What results are you seeing?


# In[9]:


#Example 3
# Find the the top 5 commodities among households
tmp = df.groupby(['household_type','commodity']).agg(total_revenue=('price',sum)).reset_index()
pd.concat(
    [tmp[tmp.household_type == hh] \
         .sort_values('total_revenue', ascending=False) \
     .head(5) for hh in tmp.household_type.unique()])


# In[10]:


#Example 3.1
#Set up top five for chart in Example 3.2
tmp = df.groupby(['household_type', 'commodity']).agg(total_revenue=('price', sum)).reset_index()
top_5 = pd.concat(
    [tmp[tmp.household_type == hh] \
         .sort_values('total_revenue', ascending=False) \
     .head(5) for hh in tmp.household_type.unique()]).reset_index(drop=True)
top_5.head()


# In[11]:


#Example3.2
#Chart the top five commodities for each household group
data = []
for d in top_5.household_type.unique():
    tmp1 = top_5[top_5.household_type==d].groupby(['commodity']).agg(revenue=('total_revenue', sum)).reset_index()
    data.append(go.Bar(x=tmp1.commodity, y=tmp1.revenue, name = d))
        
go.Figure(
    data = data,
    layout = go.Layout(
        title ='Top commodities per Household',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')


# In[12]:


#Your attempt 5
#Amend the code from Example 3.1
# The top 5 commodities among loyalty types


# In[13]:


#Your attempt 6
#Amend the code for top 5 based on loyalty from Example 3.2


# In[14]:


#Your attempt 7
#Amend the code and chart for top 5 based on loyalty from Example 3.3


# In[15]:


#Your attempt 8
#Amend the code and chart for top 15 based on loyalty from Example 3.2


# In[16]:


#Your attempt 9
#Amemd to chart top 15 commodities for loyalty based on Example 3.3


# In[17]:


#Your attempt 10
#Amemd to chart bottom 15 commodities for loyalty based on Example 3.2


# In[18]:


#Your attempt 11
#Amend to find bottom 15 products based on loyalty based on Example 3.3
#Amemd to chart top 15 commodities for loyalty


# In[19]:


# Example 4
# Find the average, median and total amounts spent by household type per basket
tmp_stats = df.groupby(['household_type', 'basket_id']).agg(total_revenue=('price', sum)).reset_index()
tmp_stats.groupby('household_type').agg(
    avg_basket_amount=('total_revenue', 'mean'),
    mdn_basket_amount=('total_revenue', 'median'),
    total_basket_amount=('total_revenue', 'sum'),
    num_baskets=('basket_id', 'count')
)


# In[20]:


#Your attempt 12
#Amend the code to find the average, median and total amounts spent by loyalty types per basket
# amounts spent by household type and basket


# In[ ]:


#Example 5
# The top 5 commodities among age bands
tmp = df.groupby(['age_band','commodity']).agg(total_revenue=('price',sum)).reset_index()
pd.concat(
    [tmp[tmp.age_band == hh] \
         .sort_values('total_revenue', ascending=False) \
     .head(5) for hh in tmp.age_band.unique()])


# In[ ]:


#Your attempt 13
#Amend the code for top selling 5 commodities based on age bands from Example 3.2


# In[ ]:


#Your attempt 14
#Chart the top selling commodities among age bands from Example 3.3


# In[ ]:


# Your attempt 15
# Find the average, median and total amounts spent by age_band per basket from Example 4

