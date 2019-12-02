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
    colors = ['b', 'y', 'g', 'r']
    fig, axes = plt.subplots(figsize=(17, 14), nrows=2, ncols=2)
    fig.subplots_adjust(wspace=0.2, hspace=0.20, top=0.85, bottom=0.05)
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
                    arrowprops=dict(arrowstyle="->"))
    plt.savefig('line_plot_time_price.jpg')
    plt.show()

def plot_radar(data):
    
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
#         ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), 
#                      horizontalalignment='center', verticalalignment='center')
        ax.plot(theta, d, color=color)
        ax.fill(theta, d, facecolor=color, alpha=0.25)

        ax.set_xticks(theta)
        ax.set_xticklabels(data.index, {'color': 'black', 'size': 12})#TODO: Replace with smaller text
        
        ax.set_yticks([min_label, 0, max_label])#assuming max_label is greater than 0
        ax.set_yticklabels(['%.1f' % min_label,"0", '%.1f' % max_label], {'color': 'grey', 'size': 9})
        ax.set_ylim(min_label, max_label)
        ax.legend([title], loc = (-0.15, -0.1))

#     fig.text(0.5, 0.965, 'Average Standardized Prices across Four Product Categories',
#              horizontalalignment='center', color='black', weight='bold',
#              size=20)
    
    plt.savefig('radar_plot_hol_price.jpg')
    plt.show()

def plot_holiday(cat1, cat2, cat3, cat4):
	_, hol_1 = cat1.holiday_correlation(2018, False)
	_, hol_2 = cat2.holiday_correlation(2018, False)
	_, hol_3 = cat3.holiday_correlation(2018, False)
	_, hol_4 = cat4.holiday_correlation(2018, False)

	frame = {'Office Products': hol_1, 'Software': hol_2, 'Electronics': hol_3, 'Toys': hol_4}
	hol_df = pd.DataFrame(frame)
	plot_radar(data = hol_df)

def time_price(cat1, cat2, cat3, cat4):
    time_price_1 = cat1.time_price(2018, False)
    time_price_2 = cat2.time_price(2018, False)
    time_price_3 = cat3.time_price(2018, False)
    time_price_4 = cat4.time_price(2018, False)

    frame = {'Office Products': time_price_1, 'Software': time_price_2, 'Electronics': time_price_3, 'Toys': time_price_4}
    time_price_df = pd.DataFrame(frame)
    plot_time_price(data = time_price_df)

if __name__ == "__main__":
    products1 = list(np.load('office_products_sorted_ph.npy', allow_pickle=True))
    products2 = list(np.load('software.npy', allow_pickle=True))
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

    plot_holiday(cat1, cat2, cat3, cat4)
    time_price(cat1, cat2, cat3, cat4)