from category_class import Category
from product_class import Product

import numpy as np
from scipy import stats
import datetime
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from workalendar.usa import UnitedStates
from operator import itemgetter
import pandas as pd
from math import pi

def plot_time_price(data):
    '''Plot standardized daily avg price history data over the chosen year for each category 

    :param data: Standardized avg price for each category for a chosen year 
    :type year: pandas Series
    ''' 

    assert isinstance(data, pd.Series)
    assert len(data.index) == 4

    colors = ['b', 'y', 'g', 'r']
    fig, axes = plt.subplots(figsize=(20, 17), nrows=2, ncols=2)
    fig.subplots_adjust(wspace=0.2, hspace=0.20, top=0.95, bottom=0.05)
    locator = mdates.MonthLocator(interval=3)
    formatter = mdates.DateFormatter('%b')
    
    cal=UnitedStates()
    #Goal: add annotations to the following four holidays: ['New year', 'Independence Day', 'Thanksgiving Day', 'Christmas Day']
    ann_labels = ['New year', 'Independence Day', 'Thanksgiving Day', 'Christmas Day']
    top_hols_dates = [hol[0] for hol in cal.holidays(data.index[0].year) if hol[1] in ann_labels] #Holidays as date_time objects
    
    xy_loc = [(0,-70), (0,100), (-100,-70), (-50,80)]
    
    for ax, data_item, color in zip(axes.flat, data.items(), colors):
        title = data_item[0]
        d = data_item[1]
        
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        
        ax.plot(d.index, d.values, color = color)
        ax.plot(d.index, np.zeros(len(d.index)), color='grey')
        ax.set_title(title,weight='bold', size=20, position=(0.5, 1.03), color = color,  
                     horizontalalignment='center', verticalalignment='center')
        
        ax.set_yticks(np.arange(-0.5,0.6,0.2))
    
        for hol, hol_date, xy_loc_2 in zip(ann_labels, top_hols_dates, xy_loc):
            if title == 'Office Products':
                ax.annotate(hol,
                    xy=(hol_date, d.loc[hol_date]), xycoords='data',
                    xytext=xy_loc_2, textcoords='offset points',
                    size=20,
                    arrowprops=dict(arrowstyle="->"))
                      
            else:
                ax.annotate('',
                    xy=(hol_date, d.loc[hol_date]), xycoords='data',
                    xytext=(-50, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="fancy"))
    plt.savefig('line_plot_time_price.jpg')
    plt.show()

def plot_radar(data):
    '''Plot standardized avg price for chosen holidays and year

    :param data: Standardized avg price for each category on chosen holidays
    :type year: pandas DataFrame
    '''

    assert isinstance(data, pd.DataFrame)
    assert len(data.columns) == 4
    assert len(data.index) == 4

    min_label = data.min().min() - 0.1
    max_label = data.max().max() + 0.1
    
    N = data.count(0)[0]
    theta = [n / float(N) * 2 * pi for n in range(N)]; theta += theta[:1]
    
    fig, axes = plt.subplots(figsize=(15,15), nrows=2, ncols=2,
                             subplot_kw=dict(polar=True))
    fig.subplots_adjust(wspace=0.33, hspace=0, top=1, bottom=0)

    colors = ['b', 'y', 'g', 'r']
    # Plot the four cases from the example data on separate axes
    for ax, hol, color in zip(axes.flat, data.items(), colors):
        title = hol[0]
        d = list(hol[1].values); d+= d[:1]

        ax.set_rgrids([-0.2, -0.6, 0, 0.4])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), color = color,  
                     horizontalalignment='center', verticalalignment='center')
        ax.plot(theta, d, color=color)
        ax.fill(theta, d, facecolor=color, alpha=0.25)

        ax.set_xticks(theta)
        ax.set_xticklabels(data.index, {'color': 'black', 'size': 12})#TODO: Replace with smaller text
        
        ax.set_yticks([min_label, 0, max_label])#assuming max_label is greater than 0
        ax.set_yticklabels(['%.1f' % min_label,"0", '%.1f' % max_label], {'color': 'grey', 'size': 9})
        ax.set_ylim(min_label, max_label)
        # ax.legend([title], loc = (-0.15, -0.1))

#     fig.text(0.5, 0.965, 'Average Standardized Prices across Four Product Categories',
#              horizontalalignment='center', color='black', weight='bold',
#              size=20)
    
    #plt.savefig('radar_plot_hol_price.jpg')
    plt.show()

def plot_holiday(cat1, cat2, cat3, cat4):
    '''For each Category object, call the holiday_correlation function function and
    call plot_radar function to plot the data on 4 subplots

    :param cat1 - cat4: Category objects to be analyzed  
    :type cat1 - cat4: Category objects
    '''

    assert isinstance(cat1, Category)
    assert isinstance(cat2, Category)
    assert isinstance(cat3, Category)
    assert isinstance(cat4, Category)

	_, hol_1 = cat1.holiday_correlation(2018, False)
	_, hol_2 = cat2.holiday_correlation(2018, False)
	_, hol_3 = cat3.holiday_correlation(2018, False)
	_, hol_4 = cat4.holiday_correlation(2018, False)

	frame = {'Office Products': hol_1, 'Software': hol_2, 'Electronics': hol_3, 'Toys': hol_4}
	hol_df = pd.DataFrame(frame)
	plot_radar(data = hol_df)

def time_price(cat1, cat2, cat3, cat4):
    '''For each Category object, call the price variation function and then call
    plot_time_price to plot the data on 4 subplots

    :param cat1 - cat4: Category objects to be analyzed  
    :type cat1 - cat4: Category objects
    '''
    assert isinstance(cat1, Category)
    assert isinstance(cat2, Category)
    assert isinstance(cat3, Category)
    assert isinstance(cat4, Category)

    time_price_1 = cat1.time_price(2018, False)
    time_price_2 = cat2.time_price(2018, False)
    time_price_3 = cat3.time_price(2018, False)
    time_price_4 = cat4.time_price(2018, False)

    frame = {'Office Products': time_price_1, 'Software': time_price_2, 'Electronics': time_price_3, 'Toys': time_price_4}
    time_price_df = pd.DataFrame(frame)
    plot_time_price(data = time_price_df)
    
def plot_average_derivative_prices(data):
    '''Plot average derivative price

    :param data: price history
    :type data: (list, pd.DataFrame, np.ndarray, pd.Series)
    '''
    assert isinstance(data, (list, pd.DataFrame, np.ndarray, pd.Series))
    colors = ['b', 'y', 'g', 'r']
    fig, axes = plt.subplots(figsize=(17, 14), nrows=2, ncols=2)
    fig.subplots_adjust(wspace=0.2, hspace=0.20, top=0.85, bottom=0.05)
    locator = mdates.MonthLocator(interval=3)
    formatter = mdates.DateFormatter('%b')
    
    for ax, data_item, color in zip(axes.flat, data.items(), colors):
        title = data_item[0]
        d = data_item[1]
        
        ax.fill_between(d.index[1:], d.values[1:], 0, where=d.values[1:] >= 0, facecolor='red', interpolate=True, alpha=0.7)
        ax.fill_between(d.index[1:], d.values[1:], 0, where=d.values[1:] <= 0, facecolor='green', interpolate=True, alpha=0.7)
        
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        
        ax.set_title(title,weight='bold', size=20, position=(0.5, 1.03), color = color,  
                     horizontalalignment='center', verticalalignment='center')
    #plt.savefig('average_derivative_prices.jpg')
    plt.show()
    
def average_derivative_prices(cat1, cat2, cat3, cat4):
    '''Plot derivative price in four subplots

    :param cat1, cat2, cat3, cat4: Each categories
    :type: Category
    '''
    assert isinstance(cat1, Category)
    assert isinstance(cat2, Category)
    assert isinstance(cat3, Category)
    assert isinstance(cat4, Category)
    adp1 = cat1.average_derivative_prices(2018)
    adp2 = cat2.average_derivative_prices(2018)
    adp3 = cat3.average_derivative_prices(2018)
    adp4 = cat4.average_derivative_prices(2018)
    
    frame = {'Office Products': adp1, 'Software': adp2, 'Electronics': adp3, 'Toys': adp4}
    adp_df = pd.DataFrame(frame)
    plot_average_derivative_prices(data = adp_df)
    
def plot_christmas_history(data):
    '''Plot christmas average price history

    :param data: price history
    :type data: (list, pd.DataFrame, np.ndarray, pd.Series)
    '''
    assert isinstance(data, (list, pd.DataFrame, np.ndarray, pd.Series))
    colors = ['b', 'y', 'g', 'r']
    fig, axes = plt.subplots(figsize=(17, 14), nrows=2, ncols=2)
    fig.subplots_adjust(wspace=0.2, hspace=0.20, top=0.85, bottom=0.05)
    
    for ax, data_item, color in zip(axes.flat, data.items(), colors):
        title = data_item[0]
        d = data_item[1]
        
        ax.plot(d.index.year, d.values, color = color)
        
        ax.set_title(title,weight='bold', size=20, position=(0.5, 1.03), color = color,  
                     horizontalalignment='center', verticalalignment='center')
    #plt.savefig('average_price_christmas.jpg')
    plt.show()
    
def christmas_history_price(cat1, cat2, cat3, cat4):
    '''Plot christmas average price history in four subplots

    :param cat1, cat2, cat3, cat4: Each categories
    :type: Category
    '''
    assert isinstance(cat1, Category)
    assert isinstance(cat2, Category)
    assert isinstance(cat3, Category)
    assert isinstance(cat4, Category)
    apc1 = cat1.average_price_christmas()
    apc2 = cat2.average_price_christmas()
    apc3 = cat3.average_price_christmas()
    apc4 = cat4.average_price_christmas()
    
    frame = {'Office Products': apc1, 'Software': apc2, 'Electronics': apc3, 'Toys': apc4}
    apc_df = pd.DataFrame(frame)
    plot_christmas_history(data = apc_df)

def plot_average_price_per_month(data):
    '''Plot average price per month

    :param data: price history
    :type data: (list, pd.DataFrame, np.ndarray, pd.Series)
    '''
    assert isinstance(data, (list, pd.DataFrame, np.ndarray, pd.Series))
    colors = ['b', 'y', 'g', 'r']
    fig, axes = plt.subplots(figsize=(17, 14), nrows=2, ncols=2)
    fig.subplots_adjust(wspace=0.2, hspace=0.20, top=0.85, bottom=0.05)
    
    for ax, data_item, color in zip(axes.flat, data.items(), colors):
        title = data_item[0]
        d = data_item[1]
        
        ax.plot(d.index, d.values, color = color)
        
        ax.set_title(title,weight='bold', size=20, position=(0.5, 1.03), color = color,  
                     horizontalalignment='center', verticalalignment='center')
    #plt.savefig('average_price_per_month.jpg')
    plt.show()
    
def average_price_per_month_price(cat1, cat2, cat3, cat4):
    '''Plot average price per month in four subplots

    :param cat1, cat2, cat3, cat4: Each categories
    :type: Category
    '''
    assert isinstance(cat1, Category)
    assert isinstance(cat2, Category)
    assert isinstance(cat3, Category)
    assert isinstance(cat4, Category)

    appm1 = cat1.average_price_per_month()
    appm2 = cat2.average_price_per_month()
    appm3 = cat3.average_price_per_month()
    appm4 = cat4.average_price_per_month()
    
    frame = {'Office Products': appm1, 'Software': appm2, 'Electronics': appm3, 'Toys': appm4}
    appm_df = pd.DataFrame(frame)
    plot_average_price_per_month(data = appm_df)


if __name__ == "__main__":
    products1 = list(np.load('office_products_sorted_ph.npy', allow_pickle=True))
    products2 = list(np.load('product_software_sorted_ph.npy', allow_pickle=True))
    products3 = list(np.load('product_electronics_sorted_ph.npy', allow_pickle=True))
    products4 = list(np.load('toy_products_sorted_ph.npy', allow_pickle=True))

    products1 = [Product(i) for i in products1]
    products2 = [Product(i) for i in products2]
    products3 = [Product(i) for i in products3]
    products4 = [Product(i) for i in products4]

    cat1 = Category(products1)
    cat2 = Category(products2)
    cat3 = Category(products3)
    cat4 = Category(products4)

    # plot_holiday(cat1, cat2, cat3, cat4)
    time_price(cat1, cat2, cat3, cat4)
    # average_derivative_prices(cat1, cat2, cat3, cat4)
    # average_price_per_month_price(cat1, cat2, cat3, cat4)
