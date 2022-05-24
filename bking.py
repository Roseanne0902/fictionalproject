
# coding: utf-8

# In[2]:


import pandas as pd
pd.__version__
import plotly.graph_objects as go


# In[3]:


import numpy as np


# In[5]:


df = pd.read_csv("booking_new.csv")
df.head(4)


# In[7]:


df.rename(columns={'Completed Time':'transaction_date'},inplace=True)


# In[8]:


df.rename(columns={'Paid by':'payment_status'},inplace=True)


# In[29]:


df.info()


# In[9]:


df['payment_status'] = df['payment_status'].astype(str)


# In[10]:


np.unique(df['payment_status'])


# In[11]:


df_1=df[df.payment_status != 'Canceled by CC']
df_1


# In[12]:


df_2=df_1[df_1.payment_status != 'Canceled by Corporate Admin']
df_2


# In[13]:


df_3=df_2[df_2.payment_status != 'Canceled by passenger']
df_3


# In[14]:


df_4=df_3[df_3.payment_status != 'Canceled by timeout']
df_4


# In[15]:


df_5=df_4[df_4.payment_status != 'Incident']


# In[16]:


df_5


# In[17]:


dfb=df_5.drop([260], axis=0)


# In[18]:


dfb.to_csv("pkup", index=False)


# In[19]:


dfb


# In[21]:


dfb1=pd.read_csv("pkup.csv")


# In[22]:


df.transaction_date=pd.to_datetime(df.transaction_date)
df['year']=df.transaction_date.dt.year
df['month']=df.transaction_date.dt.month
df['week']=df.transaction_date.dt.month
df.head(80)


# In[23]:


dff=pd.read_csv("calculations.csv")
dff


# In[30]:


top_week = dff.groupby(['week']).agg(total_revenue=('total_revenue',sum))     .sort_values('total_revenue', ascending = False).head(4)

go.Figure(
    data = go.Bar(x=top_week.index, y=top_week['total_revenue']),
    layout = go.Layout(
        title ='Top 4 weeks',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')


# In[34]:


booking= df[df.Booking ID == 'booking'].copy()
booking.groupby('week').agg(total_revenue=('actualpayment', sum)).plot();


# In[ ]:


tmp_booking = num_bookings.groupby('week').agg(total_revenue=('total_revenue', sum)).reset_index()
data_booking = go.Scatter(x=tmp_booking.week, y=tmp_booking.total_revenue)
    
go.Figure(
    data=data_beef,
    layout = go.Layout(
        title ='Booking trends',
        yaxis=dict(
            title='Revenue'
        )
    )
).show(renderer = 'iframe')  

