
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np


# ## Task 3.3.2 Cleaning customers data

# In[6]:


dfc = pd.read_csv('customers_2020_corrupted.csv')


# In[12]:


dfc.head(10)


# In[13]:


#str denotes a string to add to replace
dfc["id"] = dfc.customer_id.str.replace("Customer ", "")
dfc.head()


# In[17]:


dfc_new = dfc[["id","loyalty", "household_type", "age_band"]].copy()
dfc_new.rename(columns = {"id":"customer_id"}, inplace = True)
dfc_new.head()


# In[76]:


#dfc_new[["customer_id","loyalty", "household_type", "age_band"]].to_csv("new_customers_file.csv", index = False)


# In[10]:


np.unique(dfc_new["loyalty"])


# In[11]:


np.unique(dfc_new["household_type"])


# In[12]:


np.unique(dfc_new["age_band"])


# In[13]:


#Count the number of lines in the data frame - number of customers
len(dfc_new)


# In[15]:


#remove duplicate customers - drop Keep is a parameter of method drop duplicate. Keep first record and drop everything after/before
dfc_new.drop_duplicates(keep= 'first', inplace=True) #keep can be first, last, False


# In[16]:


#Check size of rows for customers after drop. You can see we dropped 100 rows
len(dfc_new)


# ## Example

# In[17]:


#using loyalty column and replacing Promiscious with Non-Loyalist
dfc_new.loyalty.replace("Promiscuous", "Non-Loyalist", inplace=True)
np.unique(dfc_new["loyalty"])


# In[51]:


dfc_new.head()


# In[ ]:




