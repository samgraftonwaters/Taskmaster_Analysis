import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gender_count_percent(gender_age_table):
    gender_count = gender_age_table['Gender'].value_counts().reset_index()
    gender_count.columns = ['Gender', 'Count']
    gender_count['Percent'] = (gender_count['Count'] / gender_count['Count'].sum() ) * 100
    print(gender_count)
    return(gender_count)

def gender_count_series(gender_age_table):
    gender_series = gender_age_table.groupby('Series Number')['Gender'].value_counts().reset_index()
    gender_series = gender_series.sort_values('Series Number', ascending = True)
    print(gender_series)
    return(gender_series)


def gender_count_series_bar(gender_age_table):
    gender_series_plot = gender_age_table.groupby(['Series Number', 'Gender']).size().unstack(fill_value=0)

    nb_row = gender_series_plot[gender_series_plot['Non-Binary'] == 1]
    print(nb_row)
    series = gender_series_plot.index
    x = np.arange(len(series))+1  # the label locations
    width = 0.4  # width of the bars

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)
    
    # Plot Male and Female bars side by side
    plt.bar(x - width/2, gender_series_plot['Male'], width, label='Male', color='dodgerblue', alpha = 0.8,
            edgecolor = 'black')
    plt.bar(x + width/2, gender_series_plot['Female'], width, label='Female', color='green', alpha = 0.8,
            edgecolor = 'black')
    plt.scatter(x[gender_series_plot['Non-Binary'] == 1], 
               gender_series_plot.loc[gender_series_plot['Non-Binary'] == 1, 'Non-Binary'],
               color='red', marker='D', s=100, label='Non-Binary')
    
    for i in range(len(gender_series_plot)):
        i = i + 1
        plt.text(i - 0.2, gender_series_plot['Male'][i] + 0.25, gender_series_plot['Male'][i], ha='center', fontsize=16, color='blue')
        plt.text(i + 0.2, gender_series_plot['Female'][i] + 0.25, gender_series_plot['Female'][i], ha='center', fontsize=16, color='green')

    # Labels, title, ticks
    plt.xlabel('Series', fontsize = 20)
    plt.ylabel('Count', fontsize = 20)
    plt.ylim(0, 5)
    plt.xlim(0.25, 20.75)
    plt.title('Counts of Male and Female per Series', fontsize = 25)
    plt.xticks(x, fontsize = 16)
    plt.yticks(fontsize = 16)
    # plt.set_xticklabels(series)
    plt.legend(fontsize = 18)

    plt.show()