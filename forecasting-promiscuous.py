
# coding: utf-8

# In[45]:


import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose #library for time series analysis
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import statsmodels
statsmodels.__version__


# In[46]:


df = pd.read_csv("dataset_2017_2020.csv")


# In[47]:


df.columns


# In[48]:


df['transaction_date'] = df.transaction_date.str[:10] #avoid time in date
df['t_date'] = pd.to_datetime(df.transaction_date) #convert to date format
df['t_date'] = df.t_date + pd.offsets.MonthBegin(-1) #send dates to first day of the month


# In[49]:


df.head()


# In[50]:


#Just keep a simple dataframe that will contain the time series for First Time Buer
ts = df[(df.loyalty ==  'Promiscuous')].groupby(['t_date']).agg(total_revenue=('price', sum)).reset_index()


# In[51]:


#Grab 3 years of data
training = ts.loc[ts.t_date < '2020-01-01'].set_index('t_date')


# In[52]:


training.plot();


# In[53]:


# See the components of a time series
# - Observed
# - Trend (direction)
# - Seasonal (repeated pattern)
# - Residual (noise)
ts_components = seasonal_decompose(training)
ts_components.plot();


# In[54]:


# Using mean and variance to check if time series is stationary
split = round(len(training) / 2)
x1 = training[0:split]
x2 = training[split:]
mean1= x1.mean()
mean2= x2.mean()
print("Mean 1 & 2= ", mean1[0], mean2[0])
var1=x1.var()
var2=x2.var()
print("Variance 1 & 2= ",var1[0], var2[0])


# Means are around the same value, but variances seem to be very disperse.

# We can use an statistical test to test whether the time series is stationary. It is a more robust way to check it out.

# In[55]:


# Test to check that the time series is not defined by a trend, therefore it is a stationaty time series.
# We use the Augmented Dickey-Fuller test
test_adf = adfuller(training)


# Null hypothesis: The times series is non-stationary, thus it has some time dependent structure
# 
# Alternate hypothesis: The null hypothesis is rejected. The time series is stationary, thus it doe not have time dependent structure.

# In[56]:


print('ADF test = ', test_adf[0])
print('p-value = ', test_adf[1])


# Given that the ADF value is negative and p-value < 0.05, we can reject the null hyphotesis and tell that our time series is stationary. Now we can apply a forecasting method.

# In[57]:


autocorrelation_plot(training);


# In[58]:


# fit the model
model = ARIMA(training, order=(3,0,0), freq='MS')
model_fit = model.fit(disp=0)


# In[59]:


# Test dataset
test = ts.loc[ts.t_date >= '2020-01-01'].set_index('t_date').reset_index()
test.head(10)


# In[60]:


whole = ts.set_index('t_date').squeeze().copy()
history = whole.take(range(36))
future = test.set_index('t_date').squeeze().copy()
for t in range(len(future)):
    model = ARIMA(history, order=(3,0,0), freq='MS')
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    obs = future[t]
    history = whole.take(range(36 + t+1))
    print('prediction', yhat, ', expected', obs, ', stderr', output[1], ', conf. int.', output[2])


# In[61]:


# Predict the revenue of the next 12 months (from June 2020 to May 2021)
# note we need running ARMA again so it captures the last observed value
model = ARIMA(history, order=(3,0,0), freq='MS')
model_fit = model.fit(disp=0)
output = model_fit.forecast(steps=12)


# In[62]:


output[0]


# In[63]:


output[2]


# In[ ]:





# In[ ]:




