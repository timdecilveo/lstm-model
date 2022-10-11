import pandas as pd
from pandas.core.indexes import multi
import numpy as np
import math
import os
from datetime import date
from prettytable import PrettyTable

import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score

from accuracy import Accuracy
from cot_data import CoTData
from db_calls import Database
from plots import Plots
from scale_data import ScaleData
from lstm import RNN, GD

output_cot = os.listdir("../data/output/cot")
output_merge = os.listdir("../data/output/merge")
output_merge_all = os.listdir("../data/output/merge-all")
output_prices = os.listdir("../data/output/prices")

algorithms = ['Adam', 'AdamW', 'ASGD', 'SGD']
# algorithms = ['Adadelta', 'Adagrad', 'Adam', 'AdamW', 'Adamax', 'ASGD', 'NAdam', 'RAdam', 'RMSprop', 'Rprop', 'SGD']
lookback = [1, 2, 3, 4, 5, 10]
num_rnnlayers = [2, 3, 4, 5]
num_outputs = [1]

def generate_files():
    # create data file for each security in ../data/output/..
    end_date = '2019-06-04'
    dataframe = CoTData.legacy_data()
    Database(dataframe).data_frame(end_date=end_date)

def price_chart_plots():
    for file in output_prices:
        dataframe = pd.read_csv(f"../data/output/prices/{file}")
        Plots(dataframe).ohlc_plot()

def lstm_algo(dataframe, output_data, pred, optimizer='AdamW', T=10, num_hidden=50, num_rnnlayers=2, num_outputs=1, train_mult=2, train_div=3):
    if output_data == 'cot':
        features = ['Open Interest', 'Noncommercial Long', 'Noncommercial Short', 'Noncommercial Spreads', 'Commercial Long', 'Commercial Short', 'Total Long', 'Total Short', 'Nonreportable Positions Long', 'Nonreportable Positions Short']

    if output_data == 'merge':
        features = ['Open', 'High', 'Low', 'Close', 'Noncommercial Long', 'Noncommercial Short', 'Commercial Long', 'Commercial Short']
        df_chg, open, high, low, close, non_commerical_long, non_commerical_short, commerical_long, commerical_short = ScaleData(dataframe, output_data).scale_data()
        # features = ['Open', 'High', 'Low', 'Close', 'TotalVolume', 'Open Interest', 'Noncommercial Long', 'Noncommercial Short', 'Noncommercial Spreads', 'Commercial Long', 'Commercial Short', 'Total Long', 'Total Short', 'Nonreportable Positions Long', 'Nonreportable Positions Short']
        # df_chg, open, high, low, close, volume, oi, non_commerical_long, non_commerical_short, non_commerical_spread, commerical_long, commerical_short, total_long, total_short, non_reportable_long, non_reportable_short = ScaleData(dataframe, output_data).scale_data()

    if output_data == 'prices':
        features = ['Open', 'High', 'Low', 'Close']
        df_chg, open, high, low, close = ScaleData(dataframe, output_data).scale_data()
        # features = ['Open', 'High', 'Low', 'Close', 'TotalVolume']
        # df_chg, open, high, low, close, volume = ScaleData(dataframe, output_data).scale_data()

    '''
    Need to determine which value you would like to predict:
    Most researchers try to predict the next day's (n+1) closing price. If that's the case,
    you should use the open, high, and low prices of that day to help in the prediction.
    The open price of that day is easy since it occurs at one point in time during the day,
    but the high/low price of that day is more difficult to implement in the model.
    It might make more sense to predict the open price of n+1, rather than the close price
    of n+1.
    '''
    input_data_shape = df_chg.values.shape[1]
    input_data = df_chg.values
    # remove 'nan' values
    input_data = input_data[~np.isnan(input_data)]
    # delete the 0th index until input_data.size % input_data_shape == 0
    while input_data.size % input_data_shape != 0:
        input_data = np.delete(input_data, 0)
    input_data = np.reshape(input_data, (-1, input_data_shape))
    # input_data = np.where(input_data < 0, 0, 1)

    '''
    The different target prices are listed below. Choose one value to predict:
        1) Open price of next time period
        2) High price of next time period
        3) Low price of next time period
        4) Close price of next time period
    '''
    if pred == 'open':
        targets = open.values
    if pred == 'high':
        targets = high.values
    if pred == 'low':
        targets = low.values
    if pred == 'close':
        targets = close.values
            
    targets = targets[~np.isnan(targets)]
    targets = np.reshape(targets, (-1))
    # targets = np.where(targets < 0, 0, 1)

    '''
    Shape of data is N x T x D:
        T is chosen in the function call
        D is number of columns in the input_data
        N is the length of the series - T
    '''
    # T = # T is chosen as a parameter of this function
    D = input_data.shape[1]
    N = len(input_data) - T # length of the dataframe - historical lookback window
    print(f"T: {T}; D: {D}; N: {N}")
    print('---------------')

    # Determine the size of the training set vs. testing set
    training_set_size = len(input_data) * train_mult // train_div

    # X_train is of shape training_set_size x T x D
    X_train = np.zeros((training_set_size, T, D))
    # Y_train is of shape training_set_size
    Y_train = np.zeros((training_set_size, 1))

    # Count up to training_set_size
    for i in range(training_set_size):
        '''
        Populate X_train and Y_train with values for training set
        '''
        X_train[i, :, :] = input_data[i:i+T]
        Y_train[i] = (targets[i+T] > 0)

    # X_test is of shape (N - training_set_size) x T x D
    X_test = np.zeros((N - training_set_size, T, D))
    # Y_test is of shape (N - training_set_size)
    Y_test = np.zeros((N - training_set_size, 1))

    # Count up to (N - training_set_size) -- or the size of the test set
    for j in range(N - training_set_size):
        '''
        Populate X_train and Y_train with values for training set
            i counts from training_set_size to N
                - used to offset the index
            j counts from 0 up to (N - training_set_size)
        ''' 
        i = j + training_set_size
        X_test[j, :, :] = input_data[i:i+T]
        Y_test[j] = (targets[i+T] > 0)

    # Run the RNN
    model = RNN(len(features), num_hidden, num_rnnlayers, num_outputs)
    device = model.device()
    model.to(device)

    # classification for up/down prediction
    criterion = nn.BCEWithLogitsLoss()
    # nbatch = 128
    # criterion = nn.BCEWithLogitsLoss(weight=nbatch, reduction='mean', pos_weight=None)

    # learning rate
    lr = 0.01
    # :param epochs: default set to 200
    epochs = 300

    error_message = f"Unable to implement {optimizer} optimizer algorithm."
    if optimizer == 'Adadelta':
        optimizer = torch.optim.Adadelta(model.parameters(), lr=lr)
    if optimizer == 'Adagrad':
        optimizer = torch.optim.Adagrad(model.parameters(), lr=lr)
    if optimizer == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    if optimizer == 'AdamW':
        optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    if optimizer == 'SparseAdam':
        # optimizer = torch.optim.SparseAdam(model.parameters(), lr=lr)
        raise ValueError(error_message)
    if optimizer == 'Adamax':
        optimizer = torch.optim.Adamax(model.parameters(), lr=lr)
    if optimizer == 'ASGD':
        optimizer = torch.optim.ASGD(model.parameters(), lr=lr)
    if optimizer == 'LBFGS':
        # optimizer = torch.optim.LBFGS(model.parameters(), lr=lr)
        raise ValueError(error_message)
    if optimizer == 'NAdam':
        optimizer = torch.optim.NAdam(model.parameters(), lr=lr)
    if optimizer == 'RAdam':
        optimizer = torch.optim.RAdam(model.parameters(), lr=lr)
    if optimizer == 'RMSprop':
        optimizer = torch.optim.RMSprop(model.parameters(), lr=lr)
    if optimizer == 'Rprop':
        optimizer = torch.optim.Rprop(model.parameters(), lr=lr)
    if optimizer == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    # schedule = 'lr_scheduler'
    schedule = 'early_stopping'

    # make inputs and targets
    X_train = torch.from_numpy(X_train.astype(np.float32))
    X_test = torch.from_numpy(X_test.astype(np.float32))
    y_train = torch.from_numpy(Y_train.astype(np.float32))
    y_test = torch.from_numpy(Y_test.astype(np.float32))

    # move data to GPU
    X_train, y_train = X_train.to(device), y_train.to(device)
    X_test, y_test = X_test.to(device), y_test.to(device)

    commodity_name = dataframe['Description'][0]
    print(f"{commodity_name}")
    print(f"{output_data} data")
    print(f"{T} historical time period(s)")
    print(f"{num_hidden} hidden layer(s);")
    print(f"{num_rnnlayers} rnn layer(s)")
    print(f"{num_outputs} output(s)")

    train_color = 'green'
    test_color = 'red'
    title = f"{commodity_name}-{T} historical time period(s)-{num_hidden} hidden layer(s)-{num_rnnlayers} rnn layer(s)-{num_outputs} output(s)"
    file_name = f'{commodity_name}-{T}-{num_hidden}-{num_rnnlayers}-{num_outputs}'
    # file_name = f'{commodity_name}-{optimizer}-{T}-{num_hidden}-{num_rnnlayers}-{num_outputs}'

    train_losses, test_losses, df_train_test_loss = GD(model, criterion, optimizer, X_train, y_train, X_test, y_test, epochs).full_gd(schedule)
    df_train_test_loss['commodity_name'] = commodity_name
    df_train_test_loss.to_csv(f"../data/performance/train-test-loss/loss-{file_name}.csv")

    plts = Plots(dataframe)
    # plts.scaled_data_plots(close, commodity_name, optimizer, file_name)
    plts.train_test_plots(train_losses, test_losses, train_color, test_color, file_name)

    train_acc, test_acc, df_accuracy = Accuracy(model, X_train, y_train, X_test, y_test).accuracy()
    df_accuracy.to_csv(f"../data/performance/accuracy/acc-{file_name}.csv")

def hidden(lookback, num_outputs):
    return math.floor((lookback * 2 / 3) + num_outputs)

# Run ech of the below functions for LSTM results
def merge():
    '''
    output_merge
        weekly prices of futures contract merged with weekly CoT data; merged by date
    '''
    for file in output_merge:
        df_merge = pd.read_csv(f"../data/output/merge/{file}")
        # for optimizer in algorithms:
        #     lstm_algo(
        #         dataframe=df_merge,
        #         output_data='merge',
        #         pred='open',
        #         optimizer=optimizer, 
        #         T=lookback,
        #         num_hidden=hidden(lookback, num_outputs),
        #         num_rnnlayers=num_rnnlayers,
        #         num_outputs=num_outputs
        lstm_algo(dataframe=df_merge, output_data='merge', pred='open', optimizer='Adam', T=3, num_hidden=hidden(3, 1), num_rnnlayers=2, num_outputs=1)
        # lstm_algo(dataframe=df_merge, output_data='merge', pred='open', optimizer='AdamW', T=3, num_hidden=hidden(3, 1), num_rnnlayers=2, num_outputs=1)
        # lstm_algo(dataframe=df_merge, output_data='merge', pred='open', optimizer='SGD', T=3, num_hidden=hidden(3, 1), num_rnnlayers=2, num_outputs=1)

def prices_func(lookback, num_rnnlayers, num_outputs):
    '''
    output_prices
        daily prices of futures contract
    '''
    for file in output_prices:
        df_prices = pd.read_csv(f"../data/output/prices/{file}")
        for optimizer in algorithms:
            lstm_algo(
                dataframe=df_prices,
                output_data='prices',
                pred='open',
                optimizer=optimizer, 
                T=lookback,
                num_hidden=hidden(lookback, num_outputs),
                num_rnnlayers=num_rnnlayers,
                num_outputs=num_outputs
            )

'''
Step 1: run generate_files() to create data for analysis
'''
# generate_files()

'''
Step 2: run price_chart_plots() to create charts of futures price data
'''
# price_chart_plots()

'''
Step 3: run the lstm algorithm to generate analysis
'''
merge()