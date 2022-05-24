
# coding: utf-8

# # Task 4.2.3

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
# As we said before, the native pandas plot() method is to create quick graphs, 
# with other libraries such as matplotlib we can have more control over our graphs/customize.

import seaborn as sns 
#another library to do plots

import plotly.graph_objects as go
# With this library we can create interactive graphs


# In[4]:


df = pd.read_csv('dataset_2017_2020.csv')


# - Calculate the number of unique transactions (total_baskets) every day
# - Get data ready first.

# In[5]:


df.transaction_date = pd.to_datetime(df.transaction_date) #Have to change to datetime format
df["year"] = df.transaction_date.dt.year
tmp = df.groupby(['year']).agg(total_baskets=('basket_id', pd.Series.nunique)).reset_index()
tmp.head()


# In[6]:


#Quick and dirty plot
plt.bar(tmp.year, tmp.total_baskets)


# Let's follow a process to customize our plot
# - Set a figure
# - Plot the contents
# - Set labels, legends, title, etc in the plot
# - Show the plot

# In[7]:


fig = plt.figure() #from this point, we start plotting. 
plt.bar(tmp.year, tmp.total_baskets, color='darkgreen') # color = ['green', 'yellow', 'blue', 'red']
plt.xticks(tmp.year)
plt.xlabel('Year')
plt.ylabel('Number of baskets')
plt.title('Unique baskets per year')
plt.show(); 


# Lets use seaborn to show the revenue of each department in the past 3 years

# In[8]:


#Chart1
tmp = df.groupby(['department', 'transaction_date']).agg(revenue=('price', sum)).reset_index()
#seaborn manipulates everything from a dataframe in the parameter data, then you only specify the columns to use
# hue is like a groupby, then we will have lines of different colors for each department
sns.lineplot(data=tmp, x='transaction_date', y='revenue', hue='department');


# In[9]:


#Chart2
# Let's make it pretty using matplotlib methods
plt.figure(figsize=(20,8))
sns.lineplot(data=tmp, x='transaction_date', y='revenue', hue='department');
plt.xlabel('Date')
plt.ylabel('Revenue')
x_labels = pd.date_range(tmp.transaction_date.min(),tmp.transaction_date.max(),5) # We use the method date_range to customize the number of dates in our x-axis. We only print 5 date labels
plt.xticks(x_labels);


# Now using plotly to create an interactive graph. We will plot the revenue of each department in the past 3 years. 
# 
# Note that with plotly we do not have to use matplotlib methods, we only interact with plotly methods.
# - Set data
# - Set figure
# - Set labels, labels, titles (Layout)
# - Show figure

# In[10]:


#Chart3
# We will plot the revenue of each department in the past 3 years
# We set our data first
df.groupby(['department', 'transaction_date']).agg(revenue=('price', sum)).reset_index()
data = []
#go through each department in the dataframe. See that unique() will return the unique set of departments available
for d in df.department.unique(): 
    #We use a temporal dataframe to store the revenue for each department
    tmp = df[df.department==d].groupby(['transaction_date']).agg(revenue=('price', sum)).reset_index()
    
    #In the empty list we defined above data[], we append all scatterplots. 
    #data contains a list of objects that have the values of transaction date and the sum of the revenue amongst other parameters to configure the plot
    #Other parameters include: name, color, type of line, line width, markers, 
    data.append(go.Scatter(x=tmp.transaction_date, y=tmp.revenue, name = d, line=dict(dash='dashdot')))
go.Figure(
    data=data,
    layout = go.Layout(
        title ='Department trends',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')
# Hover in the figure and you can see a tooltip with date, revenue value and department
# You can export the image from the menu on the rigth panel
# Click on a department and it will disappear from the graph
# Double click on a department and other departments will disappear from the graph.


# In[11]:


#Example1 - Amend code using Chart 1
#Plot household type revenue over time 1


# In[12]:


#Add your code below


# In[14]:


#Example 1 Amend code using Chart2
#Plot household type revenue over time 2
# Let's make it pretty and enlarge the chart using matplotlib methods


# In[15]:


#Example 1 Amend code using Chart3
#Plot household type revenue over time 3
#Create and interactive chart


# In[16]:


#Example 2 - Amend code using Chart 1
#Plot customer loyality revenue over time 1


# In[17]:


#Add your code below


# In[18]:


#Example 2 - Amend code using Chart2
#Plot customer loyality revenue over time 2
# Let's make it pretty and enlarge the chart using matplotlib methods


# In[19]:


#Example 2 - Amend code using Chart3
#Plot household type revenue over time 3
#Create and interactive chart


# In[20]:


#Example3 Amend code using Chart3
#Plot an interactive graph showing revenue per commodity
#Add code below

