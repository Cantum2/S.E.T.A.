import time
import datetime
import pandas


class Indicators:
    def __init__(self, dataset):
        self.dataset = dataset

    def compare_date(date1, date2):
        """
        Tells if the sma date is before the first date logged
        :param date1:
            represents the first date logged
        :param date2:
            is desired sma amount
        :return:
        """
        print(date2)
        new_date = datetime.datetime.strptime(date2, '%m/%d/%Y')
        if date1 < new_date:
            return True
        else:
            return False
        end

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

        # Make sure desired SMA is smaAmount days after first recorded date
        first_date = self.dataset['Date'].iloc[1]
        date_after_sma = datetime.datetime.strptime(first_date, '%m/%d/%Y')
        sma_threshold = date_after_sma + datetime.timedelta(days=sma_amount)
        sma = 0
        loop_start = 0

        if Indicators.compare_date(sma_threshold, date):
            date_wanted = datetime.datetime.strptime(date, '%m/%d/%Y')
            iteration_start_date = date_wanted - datetime.timedelta(days=sma_amount + 1)
            print(iteration_start_date)
            # get line number of starting date
            for i in range(1, len(self.dataset.index)):
                current_iter_date = datetime.datetime.strptime(self.dataset['Date'].iloc[i], '%m/%d/%Y')
                if current_iter_date == iteration_start_date:
                    loop_start = i
                    break

            print(loop_start)
            # sma calculation on close price
            for i in range(loop_start, loop_start + sma_amount):
                print(self.dataset['Close'].iloc[i])
                sma += float(self.dataset['Close'].iloc[i])
        else:
            print("Error")

        print(sma / sma_amount)
        return sma / sma_amount

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
        path = "../data_set/UGAZ_STOCK.CSV"
        df = pandas.read_csv(path, parse_dates=['Date'], index_col=['Date'])
        df['backward_ewm'] = df['Close'].ewm(span=ema_time_period, min_periods=0, adjust=False, ignore_na=False).mean()
        df = df.sort_index()
        df['ewm'] = df['Close'].ewm(span=ema_time_period, min_periods=0, adjust=False, ignore_na=False).mean()
        index = self.dataset.loc[self.dataset["Date"] == date].index[0] - 1

        return df['backward_ewm'].iloc[index]