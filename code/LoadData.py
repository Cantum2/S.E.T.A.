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

#import data
path = "../data_set/UGAZ_STOCK.CSV"
names = ['Date','Open','High','Low','Close','Adj Close']
dataset = pandas.read_csv(path, names=names)
print(dataset.describe())

#Calculate SMA
def getSMA(date, smaAmount):
    """

    :param date:
        get simple moving average for a given data
    :param smaAmount:
        be able to get various amounts of sma
    :return:
    """

