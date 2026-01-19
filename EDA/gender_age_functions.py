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
    x = np.arange(len(series))  # the label locations
    width = 0.35  # width of the bars

    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)
    
    # Plot Male and Female bars side by side
    ax.bar(x - width/2, gender_series_plot['Male'], width, label='Male', color='skyblue')
    ax.bar(x + width/2, gender_series_plot['Female'], width, label='Female', color='lightpink')
    ax.scatter(x[gender_series_plot['Non-Binary'] == 1], 
               gender_series_plot.loc[gender_series_plot['Non-Binary'] == 1, 'Non-Binary'],
               color='red', marker='D', s=100, label='Non-Binary (present)')

    # Labels, title, ticks
    ax.set_xlabel('Series')
    ax.set_ylabel('Count')
    ax.set_ylim(0, 6)
    ax.set_title('Counts of Male and Female per Series')
    ax.set_xticks(x)
    ax.set_xticklabels(series)
    ax.legend()

    plt.show()