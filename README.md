# lstm-model
# CMSI 5350 - Machine Learning
Long Short-Term Memory: A Recurrent Neural Network to Determine the Direction of Futures Prices
Author: Timothy Decilveo
University: Loyola Marymount University
Course: CMSI 5350 Machine Learning

# Abstract
Historically, investors in financial markets have used past data to decide whether to buy or sell a specific security, and recurrent neural networks offer market participants a way to apply this thinking systematically. Specifically, Long Short-Term Memory Recurrent Neural Networks (LSTM RNN) allow investors to utilize feedback connections to process data sequences, or time series data, which is the standard data set used in the financial markets. LSTMs can be valuable models for financial markets as there may be lags of unknown time between significant data points within a timer series. LSTMs can process data and maintain information about prior data points without knowing if the specific data point is relevant a priori.

This paper will provide a novel way to implement an LSTM model to predict the direction of futures market prices using historical price action and Commitment if Trader’s (COT) reports data.

# Data
Commodity Systems, Inc.:
Commodity Systems Inc. (CSI) is a low-cost information vendor of summary world financial market data. Daily/data updates on thousands of time series are supplied via the Internet at the close of each business day. 

Historical futures data was purchased from CSI dating back to 1946 in some cases, through June 2019. The futures prices have been back adjusted to provide a continuous time series that eliminates the gaps between expiring and newly active contracts. The idea of back adjusted
contracts involve concatenating historical contracts of a given commodity into the past while adjusting to smooth transitions between delivery months.

The data is proportionately adjusted by percentage or ratio terms and splicing contracts by adding or subtracting their relative differences into the past. Ratio-adjusted series prepared through ratio multiplications are unlikely to go negative, so there is seldom a need to elevate a series out of the negative territory. Contracts are joined by increasing or decreasing successively further distant contracts by a percentage to raise or lower the entire history by the same proportion. Rounding problems caused by attempts to preserve tick differentials of reported prices could occasionally push a given series into negative territory.  

Because the ratio adjustment yields a much milder descending slope of long-term prices into the past, there is less long-side trading bias captured from the data. An unbiased result that offers realism should be much preferred over a highly profitable and unbelievable result that holds more inflation contributions than any perceived trading style or expertise.  

The idea of ratio-adjusted contracts requires applying the percentage change in the price of the earlier contract with respect to the price of the current (or later) contract. Consider the above example where a five-cent difference in price between successive December and September contracts resulted in a five-cent adjustment to all past data with the traditional back adjuster. In a ratio-adjusted series, the fixed delta of five would represent a factor of 5/100 or 105% of the September price for all data in the September contract. This process would repeat at the same percentage for every contract boundary until the series ended.
 
The Ratio (Proportional) back-adjustment principles offered here were inspired by Thomas Stridman, who discussed the idea in his article "Data Pros and Cons" in the June 1998 issue of Futures Magazine. 

The futures evaluated are the Australian Dollar, Soybean Oil, British Pound, Corn, Cocoa, Canadian Dollar, WTI-Crude Oil, Cotton, U.S. Dollar Index, Euro Dollar, Feeder Cattle, 5-Year T-Note, Gold, HG Copper, Heating Oil, Japanese Yen, Coffee, Lumber, Live Cattle, Lean Hogs, Mexican Peso, Nasdaq 100, New Zealand Dollar, Natural Gas, Oats, Orange Juice, Palladium, Platinum, Rough Rice, Soybeans, Sugar #11, Swiss Franc, Silver, Soybean Meal, S&P 500, 2-Year T-Note, 10-Year T-Bonds, 30-Year T-Bonds, Wheat.

Commitment of Trader’s Reports (COT):
The Commodity Futures Trading Commission (CFTC) provides weekly data on the commitment of traders and concentration ratios in both legacy and new format for futures only and futures and options. The data used in this experiment only looked at legacy CoT data on futures only. History for this data goes back to 1986, where available. Data is updated weekly on Fridays at 5:00 pm ET. The data feed contains 32,500+ time-series, covering reports for 1,000+ futures contracts in new and legacy formats. For a complete list of Time-Series Codes included in this data feed, use: CFTC-Nasdaq-Metadata-api_key=7J7nAmAEHA2yVUZZCtsy.

The data is provided from Nasdaq Data Link’s API through the Quandl package. An API key must be obtained to retrieve data via the API. This data can also be accessed from a browser.

# Packages Used
Make sure to install the Quandl, PyTorch, Numpy, Pandas, and other packages used.

# Folder Structure
    .  
    ├── app                         # Compiled files; this is where the application is run from  
    |   ├── accuracy                # Accuracy class - calculates accuracy of model  
    |   ├── app                     # application to run the model with the data  
    |   ├── atr                     # ATR class - calculates Average True Range  
    |   ├── cot_data                # CoTData class - helps creates files used in ../data folder  
    |   ├── db_calls                # Database class - creates files used in ../data folder  
    |   ├── earlyStopping           # EarlyStopping class - early stopping class to stop the model  
    |   ├── lrScheduler             # LRScheduler class - learning rate scheduler to stop the model  
    |   ├── lstm                    # RNN class & GD class - used for building out the LSTM model  
    |   ├── plots                   # Plots class - various plots used during calculations  
    |   ├── scale_data              # ScaleData class - scales data to be used in the model  
    ├── data                        # Data files  
    |   ├── output                  # Outputs of various data files  
    |   |    |── cot                # CoT data extracted from Quandl  
    |   |    |── merge              # Prices data merged with CoT data on a weekly basis  
    |   |    |── merge-all          # Prices data merged with CoT data on a daily basis  
    |   |    |── prices             # Prices data extracted from ../prices folder  
    |   ├── performance             # Output files of the model's performance  
    |   |    |── accuracy           # Train and Test Accuracy of the model on each market  
    |   |    |── train-test-loss    # Train and Test Loss of the model on each market  
    |   ├── prices                  # Files that have open, high, low, close, and total volume data  
    ├── docs                        # Project documents  
    ├── model                       # This is where the ML model is saved  
    ├── plots                       # Output plots are saved in this folder  
    |   ├── scaled_data_plots       # Distribution plots of the scaled data  
    |   ├── train_test_plots        # Plots of the train and test data  
    ├── .gitignore                  # env file with API key ignored  
    ├── virtual_env.txt             # Discusses virtual environment  
    └── README.md

# Running the program
Inside app.py, run the following code:

    '''
    Step 1: run generate_files() to create data for analysis
    '''
    generate_files()

    '''
    Step 2: run price_chart_plots() to create charts of futures price data
    '''
    price_chart_plots()

    '''
    Step 3: run the lstm algorithm to generate analysis
    '''
    merge()