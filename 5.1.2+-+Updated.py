
# coding: utf-8

# # Module 5: Forecasting with ARMIA in Python
# 
# ## 5.1.2
# 
# ### Step 1: Load libraries
# Import the libraries we will need. These are Pandas, NumPy, MatplotLib as well as statsmodel which provides us with the ARIMA model.
# 
# *Note: we can use the **`from [library] import [function]`** syntax to import just a single function from a module, and not have to refer to it with the module name beforehand to shorten the code.*

# In[ ]:





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


# ### Step 2: Loading the data
# Import the data into a dataframe named **`df`**.

# In[2]:


#Create a dataframe based on the SuperFoodsMax dataset
df = pd.read_csv("dataset_2017_2020.csv")


# ### Step 3: Investigting the data
# Investigate our data. Here we just look at the columns in the dataframe by using hte `.columns` attribute of our dataset
# 
# *What other steps could you take to investigate and check our data?*

# In[3]:


#List the columns in the dataset
df.columns


# ### Step 4: Data Cleaning
# 
# Our `transaction_date` column contains data on a number of different days. We want to roll this data all into a single day per month to more easily analyse monthly trends.
# 
# The field is a simple text field with date and time listed. First we strip off the final characters to remove the time and only keep the first ten characters. 
# 
# Then we convert the text to a Python date format, so it can recognise the text as a date. Finally, we transform the dates to shift to the first date of the month. Pandas provides us with a function called `MonthBegin` which allows us to do this.
# 

# In[23]:


#Standardise dates in the dataframe to transform dates to the first day of the month and remove time references. 
#Note the new t_date variable
df['transaction_date'] = df.transaction_date.str[:10] #avoid time in date
df['t_date'] = pd.to_datetime(df.transaction_date) #convert to date format
df['t_date'] = df.t_date + pd.offsets.MonthBegin(-1) #send dates to first day of the month


# Now we can investigate the first rows of the dataframe to see what effect this has had. Compare the `transaction_date` and `t_date` columns.

# In[24]:


df.head(10)


# ### Step 5: Aggregate the data
# We can simplify the dataset to only contain the columns we need, and to aggregate to the monthly level. This will provide us with the time series to base our forecast on. Here, we group by date (one day per month thanks to the step above), and sum the `price` column for each month.
# 
# *Note: the `.reset_index()` function transforms the date column from an index (header column) to a proper data column. Try this command with and without this function and view the resulting dataframe `ts` to see the difference it makes.

# In[8]:


#5
#Just keep a simple dataframe that will contain the time series.
ts = df.groupby(['t_date']).agg(total_revenue=('price', sum)).reset_index()


# The new dataframe we have created and will now use is called ts.
# Let's check what it looks like:

# In[9]:


ts.head()


# ### Step 6: Build a training dataset
# We now want to split the time series into a training and a test dataset. The training data is what we feed into the forecast model to build our forecast. We save a small percentage of the data, called our "test data", so that once we build the model we can test it and see if the forecasts are similar to the actual data we have kept in our testing data.
# 
# Here, we split out the first three years of revenue (everything prior to 1 Jan 2020) to use to build our model. For ARIMA forecast models it is recommended to use full sets (i.e. full years) of data to make better forecasts. We can use the `.shape` attribute to check how many data points we have. 36 is 3 x 12, so we have three full years of data to train the model with.

# In[10]:


#Grab 3 years of data; we will eventually use this as our training data for our time series model.
training = ts.loc[ts.t_date < '2020-01-01'].set_index('t_date')
training.shape


# We can make a simple plot of the data to visually check what we have done:

# In[11]:


training.plot();


# ## *End of 5.1.2*
# 
# ---
# 
# ## 5.1.3
# The steps below align with module 5.1.3
# ### Step 7: Seasonal Decompose
# We can use the `seasonal_decompose` function from the `statsmodel` to see the components of our timeseries
# - Observed (actual data)
# - Trend (direction)
# - Seasonal (repeated patterns)
# - Residuals (noise)

# In[12]:


import pandas as pds
pds.__version__


# In[13]:


ts_components = seasonal_decompose(training)
ts_components.plot();


# ### Step 8: Check for stationarity using mean and variance
# We can check perform a rough check to see if a dataseries is stationary by comparing the mean and variance of the first half of the data to those of the second half and see if they are similar.

# In[14]:


#Split the training data in half
split = round(len(training) / 2) # Find mid-point
x1 = training[0:split] # Extract first half
x2 = training[split:]  # Extract second half

# Calculate means
mean1= x1.mean()
mean2= x2.mean()
print("Mean 1 & 2 = ", round(mean1[0]), round(mean2[0]))

# Calculate variances
var1=x1.var()
var2=x2.var()
print("Variance 1 & 2 = ",round(var1[0]), round(var2[0]))


# Means are around the same value, but variances seem to be in different ranges. This is only a rough guide, so instead we can use a statistical test to test whether the time series is stationary. It is a more robust way to check it out.
# 
# ## *End of 5.1.3*
# 
# ---
# 
# ## 5.1.4
# *The steps below align with module 5.1.4*
# 
# ### Step 9: Check for stationarity using Augmented Dickey-Fuller Test
# We can more accurately assess stationarity using the ADF test function from the `statsmodel` package. We are trying to determine between:
# 
# - Null hypothesis: The times series is non-stationary, thus it has some time dependent structure
# - Alternate hypothesis: The null hypothesis is rejected. The time series is stationary, thus it doe not have time dependent structure.
# 
# The Augmented Dickey-Fuller (ADF) function will output a number. The more negative the number is, the stronger the rejection of the null hypothesis that there is no stationarity.
# The test also provides us with a statistical figure called a ‘p-value’ which in this test indicates how confident we can be to reject the null hypothesis based on the test result.
# 
# If the p-value is less than 0.05, we can reject the null hypothesis with a high level of certainty, and so can assume our data is stationary.

# In[15]:


# Run test:
test_adf = adfuller(training)

#Output the results:
print('ADF test = ', test_adf[0])
print('p-value = ', test_adf[1])


# ### Step 10: Interpret Augmented Dickey-Fuller Test result
# Given that the ADF value is negative and p-value < 0.05, we can reject the null hyphotesis and assume that our time series is stationary. Now we are ready to apply a forecasting method.
# 

# ## *End of 5.1.4*
# 
# ---
# 
# ## 5.2.1
# *The steps below align with module 5.2.1.*
# 
# ### Step 11: Check autocorrelation to choose a p parameter for ARIMA model
# In order to help determine an appropriate number of previous observations to include in our model, we can create an autocorrelation plot. An autocorrelation plot charts how much correlation there is between a value and the previous values. When the correlation value is closer to 0, it is reveals there is randomness in our data. A correlation of 1 (or -1) means we can use the delayed series to predict the current series entirely (which is ideal and uncommon). For our ARIMA model, we look to choose a value for p which ensures we capture some correlation. 

# In[16]:


#11
# The autocorrelation plot will help us to define one of the parameters of the ARIMA model (parameter p)
# An autocorrelation is the correlation of a signal with a delayed copy of itself.
# When a correlation value is closer to 0 it is telling us that there is randomness in our data; 
# a correlation of 1 (or -1) means we can use the delayed series to predict the current series entirely (which is ideal and uncommon). 

autocorrelation_plot(training);


# In the SFM data, we can see there is a high correlation between a datapoint and the data point 12 months prior – which is expected for a supermarket. However, setting p to 12 would require a whole year’s worth of data before we could make a prediction. Instead, we can see that there is some negative autocorrelation 3 months prior (The negative correlation indicates that three months prior to a data point tends to be a very different value to the current value, which can be confirmed when plotting the data). As such, we may look to use 3 as the p parameter as a compromise between a shorter lag and the level of autocorrelation
# 
# Using **p=3** for the arima model means that data from 3 months in the past can help predict the data now.
# 
# ### Step 12: Define a test dataset
# In Step 6 we set up a training dataset to train our model with. Now we extract the rest of the data into a testing dataset to use once we have out model. The test dataset will include the last five months of our dataset. (Note this data is not part of the training data set created earlier in step 6). The test data is data not used in the training data, and has been reserved to allow us to test how well our model is working.
# 
# One guide is to use 70% of the dataset for training and 30% for testing; however, in time series, a better result is had by using full periods (in this case, years) in the training data.
# 
# In this case, we have used three full years of data as the training (2017 – 2019), and we will now try to predict what we have for the first five months of 2020.

# In[18]:


# Extract all data after and including Jan 2020.
test = ts.loc[ts.t_date >= '2020-01-01'].set_index('t_date')

# Have a look at our test datset:
print(test)


# ## *End of 5.2.1*
# 
# ---
# 
# ## 5.2.2
# *The steps below align with module 5.2.2.*
# 
# ### Step 13: Prepare data for ARIMA model
# To feed our data into the ARIMA model function, we need to transform it from a data frame into a series data type.
# Here we create data series for the whole timeseries, for the training data (here called `history`) and the test data (here called `future`).

# In[29]:


#13
# Transform our data in a series, where the index is the time series
whole = ts.set_index('t_date').squeeze().copy()
# history is going to countain our training data as a time series
history = whole.take(range(36))
# future contains the test data, also as a time series
future = test.squeeze().copy()


# ### Step 14: Run ARIMA model to forecast over our test data.
# We are now ready to build our ARIMA models, using the following parameters:
# - p=3 (based on the autocorrelation plot), 
# - d=0, i.e. no differencing required because in Step 11 we concluded our data is stationary, 
# - q=0, meaning we do not use a moving average in this model.
# 
# We now use a `for` loop. In this loop, we use the trainign data to run an ARIMA model to predict the next month, and output the results. We then step forward and add another month's data from the test data into the trainign data so we can then predict one more month ahead, repeating the process. This means we predict month by month until we get to the end of our test dataset. The results show our predicted value for each of the test data months, followed by the actual data for that month to allow us to compare how accurate the data is.

# In[40]:


for t in range(len(future)):
    
    # create our model using our dataset, specify the parameters of the method, p=3, d=0 as our data is stationary, q=0
    # parameter freq is used to define the frequency we have our data on, in this case it's MS or MonthStart
    model = ARIMA(history, order=(3,0,0), freq='MS')
    
    # use the fit method so the model is prepared with the training data
    model_fit = model.fit(disp=0)
    
    # use the forecast method to compute the predictions, in this case we just want the prediction for the next month
    # change steps value to increase the prediction range
    # Output will return three values:
    # 0 - the list of predicted values with size steps 
    # 1 - the calculated standard error of the prediction
    # 2 - the confidence interval of the prediction given the standard error
    output = model_fit.forecast(steps=1)
    
    # yhat is the value predicted by the model, in this case just one month
    yhat = output[0].round(2) 
    # stderr is the standard error of the prediction:
    stderr = output[1].round(2) 
    
    #confint is the confidnece interval given the standard error:
    confint = output[2].round(2) 
    
    # obs is the actual value observed for the predicted month, so we will compare predicted value v observed (real) value
    month = future.index[t]
    obs = future[t].round(2)
    
    # print the forecast revenue vs the observed revenue (since Jan 2020)
    print(month)
    print('prediction:', yhat, ', expected:', obs, ', stderr:', stderr, ', conf. int:', confint)
    
    # note that with each run, ARIMA will be run with the last observed value, so we just extend from the original time series
    history = whole.take(range(36 + t+1))
    


# ### Step 15: Interpret results of ARIMA models 
# Note that with each run, ARIMA will be run with the last observed value, so we just extend from the original time series to include another test data point, and re-run the model to forecast the next month.
# 
# Also note how, with each iteration, the gap between predicted and observed values is narrowing, as the model begins "learning" from newly observed data.

# ### Step 16: Forecast new data into the future.
# Until this point we have been “forecasting” months for which we knew the actual figure, to allow us to compare and assess our model. Now we move to true prediction, forecasting 12 ‘steps’ (or months) forward. The prediction is extended (through ‘steps’) to investigate data from June 2020 to May 2021, which we have no actual data for.

# In[41]:


# Predict the revenue of the next 12 months (from June 2020 to May 2021)
# note we need running ARMA again so it captures the last observed value

model = ARIMA(history, order=(3,0,0), freq='MS')
model_fit = model.fit(disp=0)
output = model_fit.forecast(steps=12)


# ### Step 17: Interpret the results of our forecast

# You can see that revenue is predicted to remain steady with little trends:

# In[42]:


output[0].round(2) # The first set of output shows the predicted values for the following twelve months.


# While we can train and make predictions with our model, the autocorrelation plot showed us that there is a random effect in our data, so the predictions done with our method will be less accurate. Just have a look at the confidence interval of the predicted values:

# In[44]:


# Confidence intervals:
output[2].round(2)


# It covers almost $3k difference (confidence intervals)! But with the more data we observe, we might be improving our prediction as it goes!

# In[ ]:




