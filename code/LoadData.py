#import libs
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import datetime
from matplotlib import dates
from Indicators import Indicators
from Prediction import Prediction


class LoadData:
    path = "../data_set/UGAZ_STOCK.CSV"
    dataset = pandas.read_csv(path)
    converted_dates = list(map(datetime.datetime.strptime, dataset['Date'], len(dataset['Date']) * ['%m/%d/%Y']))
    indicators = Indicators(dataset)
    elo = indicators.get_elo('1/31/2013')
    elo_ave = elo.ewm(span=9).mean()

    def plot_data(dataset, converted_dates, elo, elo_ave):
        plt.figure(1)
        plt.plot(converted_dates[-200:], dataset['Close'][-200:])

        plt.figure(2)
        plt.plot(converted_dates[-200:], elo[-200:])
        plt.plot(converted_dates[-200:], elo_ave[-200:])
        plt.legend()

        plt.show()

    def prepare_data( dataset, elo, elo_ave):
        print(dataset.shape)
        print(len(elo))
        print(len(elo_ave))
        dataset["Elo"] = elo
        print(dataset)
        drop_data = ['Date','Open', 'High', 'Low', 'Close', 'Sma', 'Stdev','Adj Close', 'backward_ewm', 'Macd', 'macd_strike']
        dataset = dataset.drop(drop_data, axis = 1)
        dataset = dataset.iloc[1:]
        prediction = Prediction(dataset)
        print(dataset)
        prediction.initiate_training()

    prepare_data(dataset, elo, elo_ave)
    plot_data(dataset, converted_dates, elo, elo_ave)

