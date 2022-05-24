
# coding: utf-8

# # Task 4.2.2

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("dataset_2017_2020.csv")


# Get the number of unique customers of each group.
# We use the native pandas version of nunique, this is our aggregation function over the customer_id
# It is a modification that we apply to a serie

# In[3]:


df.groupby('loyalty').agg(number_customers=('customer_id', pd.Series.nunique))


# Let's plot the number of unique customers in each group in a barplot.

# In[4]:


df.groupby('loyalty').agg(totals=('customer_id',pd.Series.nunique)).plot(kind='bar')


# - Let's plot the number of unique customers in each group in a horizontal barplot.
# - Let's put a title and we will hide the legend
# - Include ; to omit/silence/mute the output of the matplotlib object

# In[6]:


df.groupby('loyalty').agg(totals=('customer_id',pd.Series.nunique))     .plot(kind='barh', title='Loyalty groups', legend = False);


# We want to add the name of the x-axis.
# 
# We want to remove the name of the y-axis as it is redundant given the title of the graph.
# 
# To do the above, we use a particular library from matplotlib to modify the plotting area.

# In[7]:


from matplotlib import pyplot as plt
df.groupby('loyalty').agg(totals=('customer_id',pd.Series.nunique))     .plot(kind='barh', legend = False, title = 'Loyalty groups')
plt.xlabel('Number of customers')
plt.ylabel('');
plt.savefig('loyalty_groups') #Save the figure and now you can use it elsewhere


# Amend the code to find the unique number of products sold in each department

# In[9]:


#add your code here


# Amend the code to plot the commodity information

# In[11]:


#add your code here


# Amend the code to find the unique number of commodities available in private and national brands

# In[13]:


#add your code here


# Create a horizontal chart with this data

# In[15]:


#add your code here


# Amend the code to find the unique number of commodities bought by each household type

# In[17]:


#add your code here


# Plot this information

# In[19]:


#Add your code here


# Now amend the code to find the unique number of commodities bought by each age band

# In[21]:


#add your code here


# Plot this information

# In[23]:


#add your code here


# Pie chart example depicting numbers of age bands

# In[25]:


import pandas as pd
import matplotlib.pyplot as plt
import csv

df = pd.read_csv('dataset_2017_2020.csv')
df['age_band'].value_counts().plot.pie()


plt.show()


# In[ ]:





# In[ ]:




