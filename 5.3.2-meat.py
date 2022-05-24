
# coding: utf-8

# In[1]:


import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose #library for time series analysis
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import statsmodels
statsmodels.__version__


# In[2]:


df = pd.read_csv("dataset_2017_2020.csv")


# In[3]:


df.columns


# In[4]:


df['transaction_date'] = df.transaction_date.str[:10] #avoid time in date
df['t_date'] = pd.to_datetime(df.transaction_date) #convert to date format
df['t_date'] = df.t_date + pd.offsets.MonthBegin(-1) #send dates to first day of the month


# In[5]:


df.head()


# In[6]:


meat = df[df.commodity.str.lower().str.contains('meat|beef|chicken|seafood|pork')].copy()
meat.head()


# In[7]:


#Just keep a simple dataframe that will contain the time series.
ts = meat.groupby(['t_date']).agg(total_revenue=('price', sum)).reset_index()


# In[8]:


#Grab 3 years of data; we will eventually use this as our training data for our time series model.
training = ts.loc[ts.t_date < '2020-01-01'].set_index('t_date')
training.shape


# In[9]:


training.plot();


# In[10]:


# See the components of a time series
# - Observed
# - Trend (direction)
# - Seasonal (repeated pattern)
# - Residual (noise)
ts_components = seasonal_decompose(training)
ts_components.plot();


# In[11]:


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


# Means are around the same value, but variances seem to be in different ranges.

# We can use an statistical test to test whether the time series is stationary. It is a more robust way to check it out.

# In[12]:


# Test to check that the time series is not defined by a trend, therefore it is a stationaty time series.
# We use the Augmented Dickey-Fuller test
test_adf = adfuller(training)


# Null hypothesis: The times series is non-stationary, thus it has some time dependent structure
# 
# Alternate hypothesis: The null hypothesis is rejected. The time series is stationary, thus it doe not have time dependent structure.

# In[13]:


print('ADF test = ', test_adf[0])
print('p-value = ', test_adf[1])


# Given that the ADF value is negative and p-value < 0.05, we can reject the null hyphotesis and tell that our time series is stationary. Now we can apply a forecasting method.

# In[14]:


# Using p = 6 for the arima model means that data from 3 months in the past can help predict the data now.
autocorrelation_plot(training);


# In[15]:


# Define the test dataset, using the last 5 months of our dataset
# Note this data is *not* part of the training!
# Rule of thumb is using 70% of dataset for training and 30% for testing
# however in time series it's better having full periods.
# In this case we have used three full years of data as the training (2017 to 2019) and we will try to predict what we have of 2020.
test = ts.loc[ts.t_date >= '2020-01-01'].set_index('t_date')
test.head(10)


# In[16]:


# Transform our data in a series, where the index is the time series
whole = ts.set_index('t_date').squeeze().copy()
# history is going to countain our training data as a time series
history = whole.take(range(36))
# future contains the test data, also as a time series
future = test.squeeze().copy()
for t in range(len(future)):
    # create our model using our dataset, specify the parameters of the method, p=3, d=0 as our data is stationary, q=0
    # parameter freq is used to define the frequency we have our data on, in this case it's MS or MonthStart
    model = ARIMA(history, order=(6,0,0), freq='MS')
    # use the fit method so the model is prepared with the training data
    model_fit = model.fit(disp=0)
    # use the forecast method to compute the predictions, in this case we just want the prediction for the next month
    # change steps value to increase the prediction range
    # Output will return three values:
    # - the list of predicted values with size steps 
    # - the calculated standard error of the prediction
    # - the confidence interval of the prediction given the standard error
    output = model_fit.forecast(steps=1)
    # yhat is the value predicted by the model, in this case just one month
    yhat = output[0]
    # obs is the value observed for the predicted month, so we will compare predicted value v observed (real) value
    obs = future[t]
    # print the forecast revenue vs the observed revenue (since Jan 2020)
    print('prediction', yhat, ', expected', obs)
    # note that with each run, ARIMA will be run with the last observed value, so we just extend from the original time series
    history = whole.take(range(36 + t+1))


# In[17]:


#Observe that in each iteration the gap between predicted and observed values is narrowing, as it starts "learning" from newly observed data.


# In[18]:


# Predict the revenue of the next 12 months (from June 2020 to May 2021)
# note we need running ARMA again so it captures the last observed value
model = ARIMA(history, order=(6,0,0), freq='MS')
model_fit = model.fit(disp=0)
output = model_fit.forecast(steps=12)


# In[19]:


output[0] # 


# In[20]:


# While we can train and make predictions with our model, see that the autocorrelation plot is showing that there is a random effect in our data, 
# so the predictions done with our method will be less accurate. Just have a look at the confidence interval of the predicted values
# It covers almost $3k difference (confidence intervals)! But with the more data we observe, we might be improving our prediction as it goes!
output[2]


# In[ ]:




