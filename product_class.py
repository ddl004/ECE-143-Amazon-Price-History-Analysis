import numpy as np
from scipy import stats
import datetime
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from workalendar.usa import UnitedStates
from operator import itemgetter
import pandas as pd

class Product:
    '''
    Modularize each product to store each feature as an attribute of a class. 
    Attributes: 
        Mean, Max, Mode, Standard Deviation, Normalized Amazon time Price History
    Functions:
        Holidays overlaid, Ability to detect sales, Derivative of Price History, SCatter plot with various features
        Regression Function
    '''
    
    def __init__(self, product_dict):
        # TODO: Add more asserts
        assert isinstance(product_dict, dict)
        
        self.product_dict = product_dict
        d = {'amazon_time': product_dict['data']['AMAZON_time'], 'amazon_price': product_dict['data']['AMAZON']}
        self.df = pd.DataFrame(data=d)
        self._clean_data()

        self.df['normalized'] = self.normalize_prices(self.df['amazon_price'])
        self.df['standardized'] = self.standardize_prices(self.df['amazon_price'])
        
        # Check that price history is long enough to calculate derivative
        if self.df['amazon_price'].count() > 2:
            self.df['derivative'] = self.derivative_prices(self.df['amazon_price'])        

        self.mean = self.df['amazon_price'].mean()
        self.max = self.df['amazon_price'].max()
        self.min = self.df['amazon_price'].min()
        
        self.name = product_dict['title']
        
        try:
            self.type = product_dict['type']
        except:
            print("Type data not available")
        try:
            if len(product_dict['data']['COUNT_REVIEWS'] >= 10):
                self.num_reviews = np.median(product_dict['data']['COUNT_REVIEWS'][-10:]).astype(np.int32)
            else:
                self.num_reviews = product_dict['data']['COUNT_REVIEWS'][-1]

            self.rating = product_dict['data']['RATING'][-1]*100

        except:
            print("Rating and Review data not available")

        self.sale_prices, self.sale_times, self.num_sales, self.num_sales_percentage, self.sale_percentage = self.saleDetector()
        # if not self.sale_percentage:
        #     print(self.name)
        #     print(self.mean)
        #     print(self.min)

    def _clean_data(self):
        '''
        Given the initial dataframe, do the following:
            1. Groupby the day and use the mean value for that day
            2. Add in missing days without a price history, with default value NaN
            3. Fill forward (assumes that price has remained the same)
        '''

        assert(len(self.df['amazon_time']) > 0)
        assert(len(self.df['amazon_price']) > 0)    

        # Remove NaN entries so that none of the means are NaN
        self.df = self.remove_nan(self.df)
        # Groupby day and use the mean value (removes hour, min, sec)
        self.df = self.df.groupby(self.df.amazon_time.dt.date).mean()
        # Fill in missing days
        # print(self.df.index.max())
        # End-date set to december 1st, in case of sparse price history, last day of API
        idx = pd.date_range(start=self.df.index.min(), end=datetime.date(year=2019,month=12,day=1))
        self.df = self.df.reindex(idx, fill_value=None).reset_index(level=0)
        self.df = self.df.rename(columns={'index':'amazon_time'})
        # Fill forward
        self.df = self.df.fillna(method='ffill')
        assert not self.df.isnull().values.any()

    def price_holiday_correlation(self, year=2018, plot=False):
        '''Plot price history's correlation with a country's holidays

        :param year: Year for which prices are to be plotted 
        :type year: int
        :param plot: Indicates whether to plot the data or not 
        :type plot: bool
        :return: List of dates for which prices are available and their corresponding prices
        :rtype: list
        '''
        
        assert isinstance(year, int) and year <=2019
        #Plot the amazon time price history for the given year and overlay a graph of holidays on top of that
        # year_index = [iter_date.year == year for iter_date in self.product_dict['data']['AMAZON_time']]
        # year_prices = list(self.df['amazon_price'])[np.where(year_index)]
        # year_dates = self.product_dict['data']['AMAZON_time'][np.where(year_index)]
        # print('Number of price data points for the year %d: %d'% (year, len(year_dates)))
        df_year = self.df[:][self.df['amazon_time'].dt.year == year]
        
        cal=UnitedStates()
        us_holidays, _ = zip(*cal.holidays(year))
        
        holiday_prices = self.df[['amazon_time', 'standardized']][self.df['amazon_time'].dt.date.isin(us_holidays)]
        
        if plot:
            #Plot the dates against prices
            fig, ax = plt.subplots(constrained_layout=True)
            locator = mdates.AutoDateLocator()
            formatter = mdates.AutoDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            
            #Plot holiday lines
            for holiday in us_holidays:
                # plt.axvline(holiday, color = 'r')
                pass

            ax.plot(df_year['amazon_time'], df_year['standardized'])
            ax.set_title('%d Price vs Holidays plotter' % (year))
        
            # ax.plot(holiday_prices['amazon_time'], holiday_prices['standardized'], 'x', color = 'g')
            print("test")
            
#         return df_year['amazon_time'], df_year['amazon_price']
        return holiday_prices

    def remove_nan(self, product):
        '''Remove nan prices from price history

        :param product: price history 
        :type product: pd.DataFrame or pd.Series
        :return: product with nan entries removed
        :rtype: pd.DataFrame or pd.Series
        '''
        assert isinstance(product, (pd.DataFrame,pd.Series))

        return product.dropna()

    def standardize_prices(self, x):
        '''Given an iterable list of prices, standardize the prices
        Data is centered at 0 mean with unit variance

        :param x: price history
        :type x: (list, np.ndarray, pd.Series)
        :return: z-score standardized price history
        :rtype: np.ndarray
        '''

        assert isinstance(x, (list, np.ndarray, pd.Series))
        assert all(~np.isnan(i) for i in x)

        return stats.zscore(x)

    def normalize_prices(self, x):
        '''Normalize an iterable list of prices to range (0,1)

        :param x: price history
        :type x: (list, np.ndarray, pd.Series)
        :return: normalized price history
        :rtype: np.ndarray
        '''
        assert isinstance(x, (list, np.ndarray, pd.Series))
        assert all(~np.isnan(i) for i in x)

        return (x-np.min(x))/(np.max(x) - np.min(x))
    
    def derivative_prices(self, x):
        '''Derivative of price history
        
        :param x: price history
        :type x: (list, np.ndarray, pd.Series)
        # :return: derivative of price history
        :rtype: pd.Series
        '''
        assert isinstance(x, (list, np.ndarray, pd.Series))
        assert all(~np.isnan(i) for i in x)
        
        return pd.Series(np.gradient(x.values), x.index, name='gradient')

    def saleDetector(self, threshold=0.9, year=2018):
        """
        To detect the sale price and timing
        :param: threshold
        :type: dict
        :return: two list that are price and time 
        """
        assert isinstance(threshold, (int, float))
        assert 0 <= threshold <= 1
        assert isinstance(year, int) and year <=2019
        
        
        df_year = self.df[:][self.df['amazon_time'].dt.year == year]
        times = list(df_year['amazon_time'].values)
        price = list(df_year['amazon_price'].values)
        
        if(not len(price)):
            print("Data not available for this year")
            return None, None, None, None, None
            
        assert len(times) == len(price)
        
        meanValue = np.nanmean(price)
        sale_price = list()
        sale_time = list()
        num = 0
        for i in range(len(price)):
            if price[i] < meanValue*threshold:
                sale_price.append(price[i])
                sale_time.append(times[i])
                num+=1
        if len(sale_price) == 0:
            decrease_percent = 0
        else:
            decrease_percent = 1 - ((sum(sale_price)/len(sale_price)) / meanValue)
        return sale_price, sale_time, num, num / len(price), decrease_percent
        
        
if __name__ == "__main__":
    # products = list(np.load('office_products_data.npy', allow_pickle=True))
    products = list(np.load('product_electronics_sorted_ph.npy', allow_pickle=True))
    sample_product = products[24]
    product_object = Product(sample_product)
    # print(product_object.amazon_price_history)
    print(product_object.df)
    print(product_object.product_dict['title'])
    print(product_object.mean)
    print(product_object.max)
    print(product_object.min)
    print(product_object.num_reviews)
    print(product_object.rating)
    # print(product_object.saleDetector())
    # print(product_object.derivative_prices(product_object.df['amazon_price']))
    # product_object.price_holiday_correlation(2018, False)