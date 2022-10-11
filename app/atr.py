import pandas as pd

class ATR():
    def __init__(self, dataframe, n_days):
        self.dataframe = dataframe
        self.n_days = n_days

    def atr(self):
        '''
        Average True Range (ATR): Developed by J. Welles Wilder, the Average True Range (ATR) is an
            indicator that measures volatility. Aswith most of his indicators, Wilder designed ATR
            with commodities and daily prices in mind. Commodities are frequently more volatile than
            stocks. They were are often subject to gaps and limit moves, which occur when a commodity
            opens up or down its maximum allowed move for the session. A volatility formula based only
            on the high-low range would fail to capture volatility from gap or limit moves. Wilder
            created Average True Range to capture this “missing” volatility. It is important to remember
            that ATR does not provide an indication of price direction, just volatility.
        True Range Formula: 
            1) Find the Current High less the current Low
            2) Find the Current High less the previous Close (absolute value)
            3) Find the Current Low less the previous Close (absolute value)
            The maximum value of the above 3 calculations is the True Range for the day.
        ATR Formula:
            1) Take the arithmetic mean of the last N days of the True Range Values 

        ATR is not currently used in the calculations below, but may be useful as this progresses.
        '''
        df_atr = pd.DataFrame()

        self.dataframe['PrevClose'] = self.dataframe['Close'].shift(1) # shift data up by 1
        # True Range Calculation
        self.dataframe['high_low'] = self.dataframe['High'] - self.dataframe['Low']
        self.dataframe['high_prev_close'] = abs(self.dataframe['High'] - self.dataframe['PrevClose'])
        self.dataframe['low_prev_close'] = abs(self.dataframe['Low'] - self.dataframe['PrevClose'])
        df_atr['TrueRange'] = self.dataframe[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)
        df_atr['ATR'] = df_atr.rolling(self.n_days, min_periods=self.n_days).mean()

        return df_atr