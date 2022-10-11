import pandas as pd

class ScaleData():
    def __init__(self, dataframe, output_data):
        self.dataframe = dataframe
        self.output_data = output_data

    def scale_data(self):
        '''
        Financial time series data is noisy. To scale the data, we take the
        percentage change from time period N-1 to time period N.
        '''
        df_chg = pd.DataFrame()

        # shift prices
        '''
        shift data up by 1 to get the previous:
            Open, High, Low, Close, Total Volume
        '''
        self.dataframe['PrevOpen'] = self.dataframe['Open'].shift(1)
        self.dataframe['PrevHigh'] = self.dataframe['High'].shift(1)
        self.dataframe['PrevLow'] = self.dataframe['Low'].shift(1)
        self.dataframe['PrevClose'] = self.dataframe['Close'].shift(1)
        self.dataframe['PrevVolume'] = self.dataframe['TotalVolume'].shift(1)
        # calculate the percentage change
        '''
        Percentage Change = (value at time period N - value at time period N-1) / value at time period N-1
        '''
        df_chg['ReturnOpen'] = (self.dataframe['Open'] - self.dataframe['PrevOpen']) / self.dataframe['PrevOpen']
        df_chg['ReturnHigh'] = (self.dataframe['High'] - self.dataframe['PrevHigh']) / self.dataframe['PrevHigh']
        df_chg['ReturnLow'] = (self.dataframe['Low'] - self.dataframe['PrevLow']) / self.dataframe['PrevLow']
        df_chg['ReturnClose'] = (self.dataframe['Close'] - self.dataframe['PrevClose']) / self.dataframe['PrevClose']
        # df_chg['ReturnVolume'] = (self.dataframe['TotalVolume'] - self.dataframe['PrevVolume']) / self.dataframe['PrevVolume']

        open = df_chg['ReturnOpen']
        high = df_chg['ReturnHigh']
        low = df_chg['ReturnLow']
        close = df_chg['ReturnClose']
        # volume = df_chg['ReturnVolume']

        if self.output_data == 'cot' or self.output_data == 'merge':
            '''
            shift data up by 1 to get the previous:
                Open Interest, Noncommercial Long, Noncommercial Short, Commercial Long, Commercial Short,
                Total Long, Total Short, Nonreportable Positions Long, Nonreportable Positions Short
            '''
            # shift CoT data
            self.dataframe['PrevOI'] = self.dataframe['Open Interest'].shift(1) 
            self.dataframe['PrevNonCommLong'] = self.dataframe['Noncommercial Long'].shift(1)
            self.dataframe['PrevNonCommShort'] = self.dataframe['Noncommercial Short'].shift(1)
            self.dataframe['PrevNonCommSprd'] = self.dataframe['Noncommercial Spreads'].shift(1)
            self.dataframe['PrevCommLong'] = self.dataframe['Commercial Long'].shift(1)
            self.dataframe['PrevCommShort'] = self.dataframe['Commercial Short'].shift(1)
            self.dataframe['PrevTotalLong'] = self.dataframe['Total Long'].shift(1)
            self.dataframe['PrevTotalShort'] = self.dataframe['Total Short'].shift(1)
            self.dataframe['PrevNonReportPosLong'] = self.dataframe['Nonreportable Positions Long'].shift(1)
            self.dataframe['PrevNonReportPosShort'] = self.dataframe['Nonreportable Positions Short'].shift(1)
            # calculate the percentage return
            '''
            Percentage Change = (value at time period N - value at time period N-1) / value at time period N-1
            '''
            # df_chg['PercChgOI'] = (self.dataframe['Open Interest'] - self.dataframe['PrevOI']) / self.dataframe['PrevOI']
            df_chg['PercChgNonCommLong'] = (self.dataframe['Noncommercial Long'] - self.dataframe['PrevNonCommLong']) / self.dataframe['PrevNonCommLong']
            df_chg['PercChgNonCommShort'] = (self.dataframe['Noncommercial Short'] - self.dataframe['PrevNonCommShort']) / self.dataframe['PrevNonCommShort']
            # df_chg['PercChgNonCommSprd'] = (self.dataframe['Noncommercial Spreads'] - self.dataframe['PrevNonCommSprd']) / self.dataframe['PrevNonCommSprd']
            df_chg['PercChgCommLong'] = (self.dataframe['Commercial Long'] - self.dataframe['PrevCommLong']) / self.dataframe['PrevCommLong']
            df_chg['PercChgCommShort'] = (self.dataframe['Commercial Short'] - self.dataframe['PrevCommShort']) / self.dataframe['PrevCommShort']
            # df_chg['PercChgTotalLong'] = (self.dataframe['Total Long'] - self.dataframe['PrevTotalLong']) / self.dataframe['PrevTotalLong']
            # df_chg['PercChgTotalShort'] = (self.dataframe['Total Short'] - self.dataframe['PrevTotalShort']) / self.dataframe['PrevTotalShort']
            # df_chg['PercChgNonReportPosLong'] = (self.dataframe['Nonreportable Positions Long'] - self.dataframe['PrevNonReportPosLong']) / self.dataframe['PrevNonReportPosLong']
            # df_chg['PercChgNonReportPosShort'] = (self.dataframe['Nonreportable Positions Short'] - self.dataframe['PrevNonReportPosShort']) / self.dataframe['PrevNonReportPosShort']

            # oi = df_chg['PercChgOI']
            non_commerical_long = df_chg['PercChgNonCommLong']
            non_commerical_short = df_chg['PercChgNonCommShort']
            # non_commerical_spread = df_chg['PercChgNonCommSprd']
            commerical_long = df_chg['PercChgCommLong']
            commerical_short = df_chg['PercChgCommShort']
            # total_long = df_chg['PercChgTotalLong']
            # total_short = df_chg['PercChgTotalShort']
            # non_reportable_long = df_chg['PercChgNonReportPosLong']
            # non_reportable_short = df_chg['PercChgNonReportPosShort']
            # Plots.scaled_data_plots(close)

            return df_chg, open, high, low, close, non_commerical_long, non_commerical_short, commerical_long, commerical_short
            # return df_chg, open, high, low, close, volume, oi, non_commerical_long, non_commerical_short, non_commerical_spread, commerical_long, commerical_short, total_long, total_short, non_reportable_long, non_reportable_short
        
        # Plots.scaled_data_plots(close)
        else:
            return df_chg, open, high, low, close
            # return df_chg, open, high, low, close, volume