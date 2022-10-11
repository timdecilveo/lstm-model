import numpy as np
import pandas as pd
from prettytable import PrettyTable
import torch

class Accuracy:
    def __init__(self, model, X_train, y_train, X_test, y_test):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def accuracy(self):
        with torch.no_grad():
            p_train = self.model(self.X_train)
            p_train_less_than = (p_train.cpu().numpy() < 0)
            p_train = (p_train.cpu().numpy() > 0)
            train_acc = np.mean(self.y_train.cpu().numpy() == p_train)

            p_test = self.model(self.X_test)
            p_test_less_than = (p_test.cpu().numpy() < 0)
            p_test = (p_test.cpu().numpy() > 0)
            test_acc = np.mean(self.y_test.cpu().numpy() == p_test)

        df_accuracy = pd.DataFrame()
        df_accuracy['train_acc'] = [train_acc]
        df_accuracy['test_acc'] = [test_acc]
        

        train_acc = f'{train_acc:.4f}'
        test_acc = f'{test_acc:.4f}'

        table = PrettyTable()
        table.add_column('Train Accuracy', [train_acc])
        table.add_column('Test Accuracy', [test_acc])
        print(table)

        return train_acc, test_acc, df_accuracy