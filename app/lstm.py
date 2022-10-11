import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from prettytable import PrettyTable
from lrScheduler import LRScheduler
from earlyStopping import EarlyStopping

class RNN(nn.Module):
    '''
    Instantiate the model
    '''
    def __init__(self, num_inputs, num_hidden, num_rnnlayers, num_outputs):
        '''
        1) call the parent class constructor
        2) assign instance variables -> num_inputs, num_hidden, num_rnnlayers, num_outputs
        :param num_inputs:    The historical lookback window. References the amount of 
                              historical time periods to use in the analysis
        :param num_hidden:    The number of features in the hidden state
        :param num_rnnlayers: Number of recurrent layers. E.g., setting num_layers=2 would
                              mean stacking two RNNs together to form a stacked RNN, with
                              the second RNN taking in outputs of the first RNN and
                              computing the final results. Default: 1
        :param num_outputs:   
        '''
        super(RNN, self).__init__()
        self.D = num_inputs
        self.M = num_hidden
        self.L = num_rnnlayers
        self.K = num_outputs

        # declare RNN layers
        self.rnn = nn.LSTM(
            input_size = self.D,
            hidden_size = self.M,
            num_layers = self.L,
            bias=True,
            batch_first=True,
            dropout=0.2, # can be any value between 0 and 1
            bidirectional=False,
        )
        # declare final dense layer
        self.fc = nn.Linear(self.M, self.K)

    def device(self):
        '''
        set the device to cuda:0 if available
        '''
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        return device

    def forward(self, X):
        '''
        initial hidden state = h0 = L x N x M -> shape
        initial cell state = c0 = L x N x M -> shape
        :param X: 
        '''
        # Initial hidden states
        h0 = torch.zeros(self.L, X.size(0), self.M).to(self.device())
        c0 = torch.zeros(self.L, X.size(0), self.M).to(self.device())
        '''
        Outputs:
        1) X = we get the hidden value at each sample, each time step, and each feature
        2) (h0, c0) = we get the hidden state h0 and cell state c0 at the final time step
            - h0 (hidden state) will be of shape L x N x M.
            This is the hidden state at each sample, each layer, and each feature
            - c0 (cell state) will be of shape L x N x M.
            This is the cell state at each sample, each layer, and each feature
        '''
        # Get RNN unit output
        out, _ = self.rnn(X, (h0, c0))
        # Want h(T) at the final time step
        out = self.fc(out[:, -1, :])
        return out

class GD():
    '''
    
    '''
    def __init__(self,
                model,
                criterion,
                optimizer,
                X_train,
                y_train,
                X_test,
                y_test,
                epochs=200):
        '''
        :param model: 
        :param criterion: 
        :param optimizer: 
        :param X_train: 
        :param y_train: 
        :param X_test: 
        :param y_test: 
        :param epochs: default set to 200
        '''
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.epochs = epochs

    # def full_gd(self):
    def full_gd(self, schedule):
        '''
        
        '''
        # stuff to store
        train_losses = np.zeros(self.epochs)
        test_losses = np.zeros(self.epochs)

        if schedule == 'lr_scheduler':
            print('INFO: Initializing learning rate scheduler')
        if schedule =='early_stopping':
            print('INFO: Initializing early stopping')

        for it in range(self.epochs):
            # zero the parameter gradients
            self.optimizer.zero_grad()

            # forward pass
            outputs = self.model(self.X_train)
            loss = self.criterion(outputs, self.y_train)

            # backward and optimize
            loss.backward()
            self.optimizer.step()

            # save losses
            train_losses[it] = loss.item()

            # test loss
            test_outputs = self.model(self.X_test)
            test_loss = self.criterion(test_outputs, self.y_test)
            test_losses[it] = test_loss.item()


            if (it + 1) % 100 == 0:
                table = PrettyTable()
                table.add_column('Epoch', [it + 1])
                table.add_column('Train Loss', [f'{train_losses[it]:.4f}'])
                table.add_column('Test Loss', [f'{test_losses[it]:.4f}'])
                print(table)
                
            # # either initialize early stopping or learning rate scheduler
            # if schedule == 'lr_scheduler':
            #     lr_scheduler = LRScheduler(self.optimizer)
            #     lr_scheduler(test_loss)
            
            # if schedule =='early_stopping':
            #     early_stopping = EarlyStopping()
            #     early_stopping(test_loss)
                
            #     if early_stopping.early_stop:
            #         break

        df_train_test_loss = pd.DataFrame()
        ep = [x for x in range(1, self.epochs+1)]
        df_train_test_loss['Epoch'] = ep
        df_train_test_loss['TrainLoss'] = train_losses
        df_train_test_loss['TestLoss'] = test_losses
        df_train_test_loss['model'] = self.model
        df_train_test_loss['criterion'] = self.criterion
        df_train_test_loss['optimizer'] = self.optimizer
            
        return train_losses, test_losses, df_train_test_loss