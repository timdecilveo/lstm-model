'''
Commodity Futures Trading Commission Commitments of Traders (COT) Reports Website:
https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm

40 different futures markets are used to create the data set implemented in the program.

Website: https://data.nasdaq.com/data/CFTC-commodity-futures-trading-commission-reports/documentation
Data: Commitment of Traders Reports
Overview: Updated weekly, the Commodity Futures Trading Commission Reports (CFTC) data
feed offers data on commitment of traders and concentration ratios in both legacy and
new format for futures only as well as futures and options. History goes back to 1994,
where available.

Delivery: Data is updated weekly on Fridays at 5:00 pm ET. Publisher: Commitment of
Traders data for futures comes from the US Commodity Futures Trading Commission (CFTC),
an independent regulatory agency of the U.S. government. Data exists in both legacy and
new format for futures only as well as futures and options. Not all contracts have data
in every format.

Coverage & Data Organization
Coverage:
This data feed contains 32,500+ time-series, covering reports for 1,000+ futures contracts
in new and legacy formats. Historical data goes back to 1994, where available.
Data Organization:
This product can be accessed via Nasdaq Data Link's Time-Series API or from a browser,
using the following route:
  https://data.nasdaq.com/data/{Time-Series_Code}

To programmatically access individual time-series in this product via our API or libraries,
you need the Time-Series Code for the specific time-series you are interested in. Time-Series
Code Format: The Time-Series Codes for all time-series in this data feed follow the format:
  CFTC/{CONTRACT}_{MEASURE}

      CFTC is the data feed code
      {CONTRACT} refers to the specific futures contract code
      {MEASURE} refers to the type of measurement done by the CFTC
For example, let's say you're interested in CBOT Wheat futures. These have the contract
code 001602. For this specific contract, let's say you're interested in the "full commitment
of traders, futures only, new format". This has the measure type code F_ALL. Therefore the full
dataset code in this case would be CFTC/001602_F_ALL. Similarly, "Concentration ratios, futures
plus options, legacy format" (measure type code: FO_L_ALL_CR) for "VIX futures" (contract code:
1170E1) can be found under CFTC/1170E1_FO_L_ALL_CR For a complete list of Time-Series Codes
included in this data feed, use:
https://data.nasdaq.com/api/v3/databases/CFTC/metadata?api_key=7J7nAmAEHA2yVUZZCtsy
'''
class CoTData:
    def data():
        data = {
            0: {'description': 'Australian Dollar', 'symbol': 'AD', 'exchange': 'CME', 'code': '232741_F_ALL'},
            1: {'description': 'Soybean Oil', 'symbol': 'BO', 'exchange': 'CBT', 'code': '007601_F_ALL'},
            2: {'description': 'British Pound', 'symbol': 'BP', 'exchange': 'CME', 'code': '096742_F_ALL'},
            3: {'description': 'Corn', 'symbol': 'C', 'exchange': 'CBT', 'code': '002602_F_ALL'},
            4: {'description': 'Cocoa', 'symbol': 'CC', 'exchange': 'NYCE', 'code': '073732_F_ALL'},
            5: {'description': 'Canadian Dollar', 'symbol': 'CD', 'exchange': 'CME', 'code': '090741_F_ALL'},
            6: {'description': 'WTI-Crude Oil', 'symbol': 'CL', 'exchange': 'NYMEX', 'code': '067651_F_ALL'},
            7: {'description': 'Cotton', 'symbol': 'CT', 'exchange': 'NYCE', 'code': '033661_F_ALL'},
            8: {'description': 'U.S. Dollar Index', 'symbol': 'DX', 'exchange': 'CME', 'code': '098662_F_ALL'},
            9: {'description': 'Euro Dollar', 'symbol': 'ED', 'exchange': 'CME', 'code': '132741_F_ALL'},
            10: {'description': 'Feeder Cattle', 'symbol': 'FC', 'exchange': 'CME', 'code': '061641_F_ALL'},
            11: {'description': '5-Year T-Note', 'symbol': 'FV', 'exchange': 'CBT', 'code': '044601_F_ALL'},
            12: {'description': 'Gold', 'symbol': 'GC', 'exchange': 'COMEX', 'code': '088691_F_ALL'},
            13: {'description': 'HG Copper', 'symbol': 'HG', 'exchange': 'COMEX', 'code': '085692_F_ALL'},
            14: {'description': 'Heating Oil', 'symbol': 'HO', 'exchange': 'NYMEX', 'code': '022651_F_ALL'},
            15: {'description': 'Japanese Yen', 'symbol': 'JY', 'exchange': 'CME', 'code': '097741_F_ALL'},
            16: {'description': 'Coffee', 'symbol': 'KC', 'exchange': 'NYCE', 'code': '083731_F_ALL'},
            17: {'description': 'Lumber', 'symbol': 'LB', 'exchange': 'CME', 'code': '058643_F_ALL'},
            18: {'description': 'Live Cattle', 'symbol': 'LC', 'exchange': 'CME', 'code': '057642_F_ALL'},
            19: {'description': 'Lean Hogs', 'symbol': 'LH', 'exchange': 'CME', 'code': '054642_F_ALL'},
            20: {'description': 'Mexican Peso', 'symbol': 'MP', 'exchange': 'CME', 'code': '095741_F_ALL'},
            21: {'description': 'Nasdaq 100', 'symbol': 'ND', 'exchange': 'CME', 'code': '20974P_F_ALL'},
            22: {'description': 'New Zealand Dollar', 'symbol': 'NE', 'exchange': 'CME', 'code': '112741_F_ALL'},
            23: {'description': 'Natural Gas', 'symbol': 'NG', 'exchange': 'NYMEX', 'code': '023651_F_ALL'},
            24: {'description': 'Oats', 'symbol': 'O', 'exchange': 'CME', 'code': '004603_F_ALL'},
            25: {'description': 'Orange Juice', 'symbol': 'OJ', 'exchange': 'ICE', 'code': '040701_F_ALL'},
            26: {'description': 'Palladium', 'symbol': 'PA', 'exchange': 'NYMEX', 'code': '075651_F_ALL'},
            27: {'description': 'Platinum', 'symbol': 'PL', 'exchange': 'NYMEX', 'code': '076651_F_ALL'},
            28: {'description': 'Rough Rice', 'symbol': 'RR', 'exchange': 'CBT', 'code': '039601_F_ALL'},
            29: {'description': 'Soybeans', 'symbol': 'S', 'exchange': 'CBT', 'code': '005602_F_ALL'},
            30: {'description': 'Sugar #11', 'symbol': 'SB', 'exchange': 'NYCE', 'code': '080732_F_ALL'},
            31: {'description': 'Swiss Franc', 'symbol': 'SF', 'exchange': 'CME', 'code': '092741_F_ALL'},
            32: {'description': 'Silver', 'symbol': 'SI', 'exchange': 'COMEX', 'code': '084691_F_ALL'},
            33: {'description': 'Soybean Meal', 'symbol': 'SM', 'exchange': 'CBT', 'code': '026603_F_ALL'},
            34: {'description': 'S&P 500', 'symbol': 'SP', 'exchange': 'CME', 'code': '13874P_F_ALL'},
            35: {'description': '2-Year T-Note', 'symbol': 'TU', 'exchange': 'CME', 'code': '042601_F_ALL'},
            36: {'description': '10-Year T-Bonds', 'symbol': 'TY', 'exchange': 'CME', 'code': '043602_F_ALL'},
            37: {'description': 'T-Bonds', 'symbol': 'US', 'exchange': 'CBT', 'code': '020601_F_ALL'},
            38: {'description': 'Wheat', 'symbol': 'W', 'exchange': 'CBT', 'code': '001602_F_ALL'},
        }
        return data

    def legacy_data():
        data_legacy = {
            0: {'description': 'Australian Dollar', 'symbol': 'AD', 'exchange': 'CME', 'code': '232741_F_L_ALL'},
            1: {'description': 'Soybean Oil', 'symbol': 'BO', 'exchange': 'CBT', 'code': '007601_F_L_ALL'},
            2: {'description': 'British Pound', 'symbol': 'BP', 'exchange': 'CME', 'code': '096742_F_L_ALL'},
            3: {'description': 'Corn', 'symbol': 'C', 'exchange': 'CBT', 'code': '002602_F_L_ALL'},
            4: {'description': 'Cocoa', 'symbol': 'CC', 'exchange': 'NYCE', 'code': '073732_F_L_ALL'},
            5: {'description': 'Canadian Dollar', 'symbol': 'CD', 'exchange': 'CME', 'code': '090741_F_L_ALL'},
            6: {'description': 'WTI-Crude Oil', 'symbol': 'CL', 'exchange': 'NYMEX', 'code': '067651_F_L_ALL'},
            7: {'description': 'Cotton', 'symbol': 'CT', 'exchange': 'NYCE', 'code': '033661_F_L_ALL'},
            8: {'description': 'U.S. Dollar Index', 'symbol': 'DX', 'exchange': 'CME', 'code': '098662_F_L_ALL'},
            9: {'description': 'Euro Dollar', 'symbol': 'ED', 'exchange': 'CME', 'code': '132741_F_L_ALL'},
            10: {'description': 'Feeder Cattle', 'symbol': 'FC', 'exchange': 'CME', 'code': '061641_F_L_ALL'},
            11: {'description': '5-Year T-Note', 'symbol': 'FV', 'exchange': 'CBT', 'code': '044601_F_L_ALL'},
            12: {'description': 'Gold', 'symbol': 'GC', 'exchange': 'COMEX', 'code': '088691_F_L_ALL'},
            13: {'description': 'HG Copper', 'symbol': 'HG', 'exchange': 'COMEX', 'code': '085692_F_L_ALL'},
            14: {'description': 'Heating Oil', 'symbol': 'HO', 'exchange': 'NYMEX', 'code': '022651_F_L_ALL'},
            15: {'description': 'Japanese Yen', 'symbol': 'JY', 'exchange': 'CME', 'code': '097741_F_L_ALL'},
            16: {'description': 'Coffee', 'symbol': 'KC', 'exchange': 'NYCE', 'code': '083731_F_L_ALL'},
            17: {'description': 'Lumber', 'symbol': 'LB', 'exchange': 'CME', 'code': '058643_F_L_ALL'},
            18: {'description': 'Live Cattle', 'symbol': 'LC', 'exchange': 'CME', 'code': '057642_F_L_ALL'},
            19: {'description': 'Lean Hogs', 'symbol': 'LH', 'exchange': 'CME', 'code': '054642_F_L_ALL'},
            20: {'description': 'Mexican Peso', 'symbol': 'MP', 'exchange': 'CME', 'code': '095741_F_L_ALL'},
            21: {'description': 'Nasdaq 100', 'symbol': 'ND', 'exchange': 'CME', 'code': '20974P_F_L_ALL'},
            22: {'description': 'New Zealand Dollar', 'symbol': 'NE', 'exchange': 'CME', 'code': '112741_F_L_ALL'},
            23: {'description': 'Natural Gas', 'symbol': 'NG', 'exchange': 'NYMEX', 'code': '023651_F_L_ALL'},
            24: {'description': 'Oats', 'symbol': 'O', 'exchange': 'CME', 'code': '004603_F_L_ALL'},
            25: {'description': 'Orange Juice', 'symbol': 'OJ', 'exchange': 'ICE', 'code': '040701_F_L_ALL'},
            26: {'description': 'Palladium', 'symbol': 'PA', 'exchange': 'NYMEX', 'code': '075651_F_L_ALL'},
            27: {'description': 'Platinum', 'symbol': 'PL', 'exchange': 'NYMEX', 'code': '076651_F_L_ALL'},
            28: {'description': 'Rough Rice', 'symbol': 'RR', 'exchange': 'CBT', 'code': '039601_F_L_ALL'},
            29: {'description': 'Soybeans', 'symbol': 'S', 'exchange': 'CBT', 'code': '005602_F_L_ALL'},
            30: {'description': 'Sugar #11', 'symbol': 'SB', 'exchange': 'NYCE', 'code': '080732_F_L_ALL'},
            31: {'description': 'Swiss Franc', 'symbol': 'SF', 'exchange': 'CME', 'code': '092741_F_L_ALL'},
            32: {'description': 'Silver', 'symbol': 'SI', 'exchange': 'COMEX', 'code': '084691_F_L_ALL'},
            33: {'description': 'Soybean Meal', 'symbol': 'SM', 'exchange': 'CBT', 'code': '026603_F_L_ALL'},
            34: {'description': 'S&P 500', 'symbol': 'SP', 'exchange': 'CME', 'code': '13874P_F_L_ALL'},
            35: {'description': '2-Year T-Note', 'symbol': 'TU', 'exchange': 'CME', 'code': '042601_F_L_ALL'},
            36: {'description': '10-Year T-Bonds', 'symbol': 'TY', 'exchange': 'CME', 'code': '043602_F_L_ALL'},
            37: {'description': 'T-Bonds', 'symbol': 'US', 'exchange': 'CBT', 'code': '020601_F_L_ALL'},
            38: {'description': 'Wheat', 'symbol': 'W', 'exchange': 'CBT', 'code': '001602_F_L_ALL'},
        }
        return data_legacy