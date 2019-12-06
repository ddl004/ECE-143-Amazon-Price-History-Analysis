from product_class import Product

import numpy as np
from scipy import stats
import datetime
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from workalendar.usa import UnitedStates
from operator import itemgetter
import pandas as pd

class Category:
    '''
        Represent a list of products in a given category
    '''

    def __init__(self, product_list):
        assert isinstance(product_list, (list, Product))
        if isinstance(product_list, list):
            assert all(isinstance(i, Product) for i in product_list)

        self.product_list = product_list
        self.num_sales, self.percent_sale = self.calculate_avg_num_sales()
        self.sale_decrease_percentage = self.calculate_avg_sale_perc()

    def calculate_avg_num_sales(self, year=2018):
        '''Calculate number of sales for products in category
        
        :return: the average number and percentage of sale of the category
        :rtype: int, float
        '''
        assert isinstance(year, int) and year <=2019
        
        num = list()
        percents = list()
        for i in range(len(self.product_list)):
            sale, time, number, pct, decrease = self.product_list[i].saleDetector(year=year)
            if number != None and pct != None:
                num.append(number)
                percents.append(pct)
                  
        res_num = sum(num)/len(num)
        res_percent = sum(percents)/len(percents)
        
        return res_num, res_percent
        

    def calculate_avg_sale_perc(self, year=2018):
        '''Calculate avg sale percentage for products in category
        
        :return: the avg sale percentage(e.g. X% off)
        :rtype: float
        '''
        assert isinstance(year, int) and year <=2019

        decrese_list = list()
        for i in range(len(self.product_list)):
            sale, time, number, pct, decrease = self.product_list[i].saleDetector(year=year)
            if decrease != 0 and decrease != None:
                decrese_list.append(decrease)
        
        return sum(decrese_list)/len(decrese_list)
        

    def price_variation(self):
        '''Calculate price variation using standardized price values
        
        :return: a list of price variation on standarized price values
        :rtype: list 
        '''
        price_variation_list = list()
        for p in self.product_list:
            price_variation_list.append(p.df.standardized.diff().fillna(0))
        return price_variation_list 

    def feature_correlation(self, feature_1, feature_2):
        '''Generate a plot for the category, showing the correlation between two features
        
        :param feature_1: [description]
        :type feature_1: [type]
        :param feature_2: [description]
        :type feature_2: [type]
        :return: feature 1 and feature 2 for all products
        :rtype: list 
        '''
        assert isinstance(feature_1, str)
        assert isinstance(feature_2, str)
        
        x = [getattr(product, feature_1) for product in self.product_list]
        y = [getattr(product, feature_2) for product in self.product_list]

        assert len(x) == len(y)

        return x,y

        
        
    def holiday_correlation(self, year=2018, plot=False):
        '''Plot standardized avg price history correlation with a country's holidays

        :param year: Year for which prices are to be plotted 
        :type year: int
        :param plot: Indicates whether to plot the data or not 
        :type plot: bool
        :return: List of dates for which prices are available and their corresponding prices
        :rtype: list
        '''
        top_hols = ['New year', 'Independence Day', 'Thanksgiving Day', 'Christmas Day']
        cal = UnitedStates()
        top_hols_dates = [hol[0] for hol in cal.holidays(year) if hol[1] in top_hols]

        holiday_df = self.product_list[0].price_holiday_correlation(year)
        for i, product in enumerate(self.product_list[1:]):
            sufix = ("_%d" % i, "_%d" % (i+1))
            holiday_df = pd.merge_ordered(holiday_df, product.price_holiday_correlation(), on='amazon_time', suffixes = sufix)
        
        holiday_df = holiday_df.loc[holiday_df['amazon_time'].isin(top_hols_dates)]
        holiday_avg = holiday_df.mean(1)
        holiday_avg.index = top_hols
        if plot:
            self.plot_radar(holiday_avg)
        
        return holiday_df, holiday_avg

    def time_price(self, year=2018, plot=False):
        standard_df = self.product_list[0].df[['amazon_time', 'standardized']][self.product_list[0].df['amazon_time'].dt.year == year]
        for i, product in enumerate(self.product_list[1:]):
            suffix = ("_%d" % i, "_%d" % (i+1))
            standard_df = pd.merge_ordered(standard_df, product.df[['amazon_time', 'standardized']][product.df['amazon_time'].dt.year == year], on='amazon_time', suffixes=suffix)
        standard_df = standard_df.set_index(['amazon_time'])
        standard_df = standard_df.mean(1)
        return standard_df
    
    def average_derivative_prices(self, year=2018):
        '''Calculate derivative standardized avg price history

        :param year: Year for which prices are to be processed
        :type year: int
        :return: List of dates for which prices are available and their corresponding derivative of prices
        :rtype: list
        '''
        assert isinstance(year, int) and year <=2019
        prices_df = self.product_list[0].df[['amazon_time', 'standardized']][self.product_list[0].df['amazon_time'].dt.year == year]
        for i, product in enumerate(self.product_list[1:]):
            suffix = ("_%d" % i, "_%d" % (i+1))
            prices_df = pd.merge_ordered(prices_df, product.df[['amazon_time', 'standardized']][product.df['amazon_time'].dt.year == year], on='amazon_time', suffixes=suffix)
        prices_df = prices_df.set_index(['amazon_time'])
        prices_df = prices_df.mean(1)
        prices_df = prices_df.diff().fillna(0)
        return prices_df
    
    def average_price_christmas(self):
        '''Calculate standardized avg price history of each Christmas

        :return: List of Christmas dates for which prices are available and their corresponding average prices
        :rtype: list
        '''

        christmas_df = self.product_list[0].df[['amazon_time', 'standardized_all']][(self.product_list[0].df['amazon_time'].dt.day == 25) & (self.product_list[0].df['amazon_time'].dt.month == 12)]
        for i, product in enumerate(self.product_list[1:]):
            suffix = ("_%d" % i, "_%d" % (i+1))
            christmas_df = pd.merge_ordered(christmas_df, product.df[['amazon_time', 'standardized_all']][(product.df['amazon_time'].dt.day == 25) & (product.df['amazon_time'].dt.month == 12)], on='amazon_time', suffixes=suffix)
        christmas_df = christmas_df.set_index(['amazon_time'])
        
        christmas_df = christmas_df.mean(axis=1)
        return christmas_df

    def average_price_per_month(self, year=2018):
        '''Calculate standardized avg price history

        :param year: Year for which prices are to be processed
        :type year: int
        :return: List of months for which prices are available and their corresponding average prices
        :rtype: list
        '''
        assert isinstance(year, int) and year <=2019

        prices_df = self.product_list[0].df[['amazon_time', 'standardized_all']][self.product_list[0].df['amazon_time'].dt.year == year]
        for i, product in enumerate(self.product_list[1:]):
            suffix = ("_%d" % i, "_%d" % (i+1))
            prices_df = pd.merge_ordered(prices_df, product.df[['amazon_time', 'standardized_all']][product.df['amazon_time'].dt.year == year], on='amazon_time', suffixes=suffix)
        prices_df = prices_df.set_index(['amazon_time'])
        prices_df = prices_df.mean(1)
        prices_df = prices_df.groupby(prices_df.index.month).mean()
        prices_df.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return prices_df
    
if __name__ == "__main__":
    products = list(np.load('product_electronics_sorted_ph.npy', allow_pickle=True))
    products = [Product(i) for i in products]
    cat = Category(products)
    # print(cat.average_price_per_month())
    print(cat.average_price_christmas())
    # print(cat.num_sales)
    # print(cat.sale_decrease_percentage)
    # cat.feature_correlation('rating','sale_percentage')
    # print(len(cat.product_list))
    # cat.holiday_correlation(2018, False)
    # b = cat.price_variation()
    # print(b)