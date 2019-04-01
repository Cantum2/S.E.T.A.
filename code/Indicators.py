import time
import datetime
import pandas
pandas.options.mode.chained_assignment = None  # default='warn'


class Indicators:
    def __init__(self, dataset):
        self.dataset = dataset

    # Calculate SMA
    def get_sma(self, date, sma_amount):
        """
         :param date:
             get simple moving average for a given data
             Must be entered in MM/DD/YYYY
         :param sma_amount:
             be able to get various amounts of sma (e.g. 9 or 16)
         :return:
            sma for the desired date
         """
        self.dataset["Sma"] = self.dataset['Close'].rolling(sma_amount).mean()
        index = self.dataset.loc[self.dataset['Date'] == date].index[0]
        print("SMA: ", self.dataset['Sma'].iloc[index])
        return self.dataset['Sma'].iloc[index]

    #Have to reread data to organize for ema
    def get_ema(self, date, ema_time_period):
        """
        :param date:
            date for specific day
        :param ema_time_period:
            20, 26, 12
        :return:
            ema for the input date
        """
        self.dataset['backward_ewm'] = self.dataset['Close'].ewm(span=ema_time_period, min_periods=0, adjust=False, ignore_na=False).mean()
        index = self.dataset.loc[self.dataset["Date"] == date].index[0]
        print("EMA:",self.dataset['backward_ewm'].iloc[index])
        return self.dataset['backward_ewm'].iloc[index]

    def get_macd(self, date):
        """
        :param date:
            date in format m/d/yyyy
        :return:
            macd for specified date
        """
        ema_26 = Indicators.get_ema(self, date, 26)
        ema_12 = Indicators.get_ema(self, date, 12)
        macd = ema_12 - ema_26
        print("MACD:",macd)
        return macd

    def get_macd_signal(self, date):
        """
        :param date:
             date in format m/d/yyyy
        :return:
            macd signal line for a specific date
        """
        index = self.dataset.loc[self.dataset["Date"] == date].index[0]
        #data is currently limited for time constraints
        for i in range(26, index+1):
            iteration_date = self.dataset['Date'].iloc[i]
            print("Date", iteration_date)
            self.dataset.loc[i, 'Macd'] = Indicators.get_macd(self, iteration_date)

        self.dataset['macd_strike'] = self.dataset['Macd'].ewm(span=9, min_periods=0, adjust=False, ignore_na=False).mean()
        print("Macd Strike: ",self.dataset['macd_strike'].iloc[index])
        return self.dataset['macd_strike'].iloc[index]

    def get_macd_hist(self, date):
        """
        :param date:
            date in format m/d/yyyy
        :return:
            macd hist for date wanted
        """
        macd = Indicators.get_macd(self, date)
        macd_signal = Indicators.get_macd_signal(self, date)

        macd_hist = macd - macd_signal
        print("Macd_hist: ",macd_hist)
        return macd_hist

    def get_bollinger_top(self, date):
        """
        :param date:
            date in format m/d/yyyy
        :return:
            top band for specific date
        """
        twenty_sma = Indicators.get_sma(self, date, 20)
        self.dataset["Stdev"] = self.dataset["Close"].rolling(20).std()
        index = self.dataset[self.dataset["Date"] == date].index[0]
        print(index)
        boll_top = twenty_sma + (self.dataset["Stdev"].iloc[index] * 2)
        print(boll_top)
        return boll_top

    def get_bollinger_bot(self, date):
        """
        :param date:
            date in format m/d/yyyy
        :return:
            top band for specific date
        """
        twenty_sma = Indicators.get_sma(self, date, 20)
        self.dataset["Stdev"] = self.dataset["Close"].rolling(20).std()
        index = self.dataset[self.dataset["Date"] == date].index[0]
        print(self.dataset.iloc[index])
        boll_bot = twenty_sma - (self.dataset["Stdev"].iloc[index] * 2)
        print(boll_bot)
        return boll_bot

    def get_rsi(self, date):
        """
        :param date:
         date in format m/d/yyyy
        :return:
            rsi value for a wanted date
        """
        index = self.dataset[self.dataset["Date"] == date].index[0]
        print(self.dataset)
        print(index)
        delta = self.dataset['Adj Close'].diff()
        dUp, dDown = delta.copy(), delta.copy()
        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0

        RolUp = dUp.ewm(span = 14).mean()
        RolDown = dDown.ewm(span = 14).mean().abs()

        RS = RolUp / RolDown
        print("RS", RS)
        RSI = 100.0 - (100.0 / (1.0+RS))
        print("RSI:",RSI)
        return RSI








