from product_class import Product

import numpy as np
# from scipy import stats
# import datetime
# import matplotlib.dates as mdates
# from matplotlib import pyplot as plt
# from workalendar.usa import UnitedStates
# from operator import itemgetter
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
        num = list()
        percents = list()
        for i in range(len(product_list)):
            sale, time, number, pct, decrease = saleDetector(product_list[i])
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
        decrese_list = list()
        for i in range(len(product_list)):
            sale, time, number, pct, decrease = saleDetector(product[i])
            if decrease != 0:
                decrese_list.append(decrease)
        return sum(decrese_list)/len(decrese_list)
        

    def price_variation(self):
        '''Calculate price variation using standardized price values
        
        :return: [description]
        :rtype: [type]
        '''

    def feature_correlation(self, feature_1, feature_2):
        '''Generate a plot for the category, showing the correlation between two features
        
        :return: [description]
        :rtype: [type]
        '''


if __name__ == "__main__":
    products = list(np.load('product_electronics_50_price_history.npy', allow_pickle=True))
    products = [Product(i) for i in products]
    cat = Category(products)
    print(len(cat.product_list))