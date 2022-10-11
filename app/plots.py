import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

class Plots:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def ohlc_plot(self):
        hovertext = []
        for i in range(len(self.dataframe['Open'])):
            hovertext.append(f"Open: {str(self.dataframe['Open'][i])}<br>High: {str(self.dataframe['High'][i])}<br>Low: {str(self.dataframe['Low'][i])}<br>Close: {str(self.dataframe['Close'][i])}<br>")

        ohlc=go.Figure(
            data=[
                go.Ohlc(
                    x=self.dataframe['Date'],
                    open=self.dataframe[('Open')],
                    high=self.dataframe[('High')],
                    low=self.dataframe[('Low')],
                    close=self.dataframe[('Close')],
                    text=hovertext,
                    hoverinfo='text',
                )
            ]
        )
        ohlc.update_xaxes(
            title_text='Date',
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label='1M', step='month', stepmode='backward'),
                        dict(count=6, label='6M', step='month', stepmode='backward'),
                        dict(count=1, label='YTD', step='year', stepmode='todate'),
                        dict(count=1, label='1Y', step='year', stepmode='backward'),
                        dict(step='all'),
                    ]
                )
            )
        )
        ohlc.update_layout(
            title={
                'text': f"{self.dataframe['Description'][0]} Price (1986-2020)",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            }
        )
        ohlc.update_yaxes(title_text=f"{self.dataframe['Description'][0]} Close Price", tickprefix='$')
        ohlc.show()

    def scaled_data_plots(self, ohlc, commodity_name, optimizer, file_name):
        plt.figure()
        plt.plot(ohlc) # plot the percentage returns
        plt.title(f'{commodity_name}-{optimizer}\nClose to Close % Returns')
        # need to figure out how to add {optimizer} to savefig
        plt.savefig(f"../plots/scaled_data_plots/perc_returns/{file_name}.png")

        plt.figure()
        ohlc.hist() # plot a histogram of the distribution of returns
        plt.title(f'{commodity_name}-{optimizer}\nClose to Close Histograms')
        # need to figure out how to add {optimizer} to savefig
        plt.savefig(f"../plots/scaled_data_plots/histograms/{file_name}.png")

        # plt.show(block=True)

    def train_test_plots(self, train_losses, test_losses, train_color, test_color, file_name):
        plt.figure()
        plt.plot(train_losses, color=train_color, label='train loss')
        plt.plot(test_losses, color=test_color, label='test loss')
        plt.title(file_name)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        # need to figure out how to add {optimizer} to savefig
        plt.savefig(f"../plots/train_test_plots/{file_name}.png")

        # plt.show(block=True)