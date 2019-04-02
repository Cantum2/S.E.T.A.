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

#import data
path = "../data_set/UGAZ_STOCK.CSV"
names = ['Date','Open','High','Low','Close','Adj Close']

dataset = pandas.read_csv(path)

converted_dates = list(map(datetime.datetime.strptime, dataset['Date'], len(dataset['Date'])*['%m/%d/%Y']))


indicators = Indicators(dataset)
indicators.get_sma("1/31/2013", 9)
indicators.get_ema("1/31/2013", 20)
#indicators.get_macd("1/31/2013")
#indicators.get_macd_signal("1/31/2013")
#indicators.get_macd_hist("1/31/2013")
#indicators.get_bollinger_top("1/31/2013")
#indicators.get_bollinger_bot("1/31/2013")
#indicators.get_rsi('1/31/2013')
elo = indicators.get_elo('1/31/2013')
elo_ave = elo.ewm(span = 9).mean()

plt.figure(1)
plt.plot(converted_dates[-200:], dataset['Close'][-200:])

plt.figure(2)
plt.plot(converted_dates[-200:], elo[-200:])
plt.plot(converted_dates[-200:], elo_ave[-200:])
plt.legend()

plt.show()


