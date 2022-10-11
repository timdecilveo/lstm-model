import pandas as pd
import numpy as np
import quandl
import os
from dotenv import load_dotenv

class Database:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def data_frame(self, start_date=None, end_date=None):

        load_dotenv()
        API_KEY = os.getenv("API_KEY") # API from env file here
        quandl.ApiConfig.api_key = API_KEY # set Quandl API key to API_KEY from env file

        prices_directory = '../data/prices/'
        descriptions = [] # array for security descriptions
        symbols = [] # array for security symbols
        exchanges = [] # array for security exchanges
        codes = [] # array for security cot report codes

        for i in self.dataframe:
            # Loop through dataframe and append symbols and codes to relevant arrays
            descriptions.append(self.dataframe[i]['description'])
            symbols.append(self.dataframe[i]['symbol'])
            exchanges.append(self.dataframe[i]['exchange'])
            codes.append(self.dataframe[i]['code'])

        for (description, symbol, exchange, code) in zip(descriptions, symbols, exchanges, codes):
            # Loop through symbols to read in txt files
            # Loop through codes to read in cot report data from quandl
            df_symbols_data = pd.read_csv(prices_directory + symbol + ".txt", sep=",", index_col='Date')
            df_cot_report_data = quandl.get('CFTC/' + code, start_date=start_date, end_date=end_date)

            # Convert df_symbols_data index to datetime format
            df_symbols_data.index = pd.to_datetime(df_symbols_data.index)

            # Merge df_symbols_data and df_cot_report_data on the 'Date' columns
            # This provides weekly data
            df_prices_cot = pd.merge(df_symbols_data, df_cot_report_data, left_on='Date', right_on='Date')
            
            # Merge df_symbols_data and df_cot_report_data on the 'Date' columns and keep all rows
            # This merges all of the data and keeps rows that have NA values
            df_prices_cot_all = pd.merge(df_symbols_data, df_cot_report_data, on=['Date'], how='outer')

            try:
                df_cot_report_data.to_csv(f"../data/output/cot/{symbol}-{description}-cot.csv")
                df_symbols_data.to_csv(f"../data/output/prices/{symbol}-{description}-prices.csv")
                df_prices_cot.to_csv(f"../data/output/merge/{symbol}-{description}-prices-cot.csv")
                df_prices_cot_all.to_csv(f"../data/output/merge-all/{symbol}-{description}-prices-cot-all.csv")
                print("-----------------------------------")
                print(f".csv file created for {symbol}-{description}-cot.")
                print(f".csv file created for {symbol}-{description}-prices.")
                print(f".csv file created for {symbol}-{description}-prices-cot.")
            except:
                print("Output error")