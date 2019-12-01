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

    def calculate_avg_num_sales(self):
        '''Calculate number of sales for products in category
        
        :return: the average number and percentage of sale of the category
        :rtype: int, float
        '''
        # TODO: Add year as input

        num = list()
        percents = list()
        for i in range(len(self.product_list)):
            sale, time, number, pct, decrease = Product.saleDetector(self.product_list[i])
            num.append(number)
            percents.append(pct)
                  
        res_num = sum(num)/len(num)
        res_percent = sum(percents)/len(percents)
        
        return res_num, res_percent
        

    def calculate_avg_sale_perc(self):
        '''Calculate avg sale percentage for products in category
        
        :return: the avg sale percentage(e.g. X% off)
        :rtype: float
        '''
        # TODO: Add year as input

        decrese_list = list()
        for i in range(len(self.product_list)):
            sale, time, number, pct, decrease = Product.saleDetector(self.product_list[i])
            if decrease != 0:
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
        '''
        assert isinstance(feature_1, str)
        assert isinstance(feature_2, str)
        
        x = [getattr(product, feature_1) for product in self.product_list]
        y = [getattr(product, feature_2) for product in self.product_list]

        assert len(x) == len(y)

        plt.scatter(x,y)

        
        
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

        hol_prices = holiday_df if holiday_df['amazon_time'] in top_hols_dates

        print(holiday_df.head())
        pritn('test')
        return holiday_df


if __name__ == "__main__":
    products = list(np.load('product_electronics_sorted_ph.npy', allow_pickle=True))
    products = [Product(i) for i in products]
    cat = Category(products)
    cat.feature_correlation('rating','sale_percentage')
    # print(len(cat.product_list))
    # cat.holiday_correlation(2018, False)
    # b = cat.price_variation()
    # print(b)