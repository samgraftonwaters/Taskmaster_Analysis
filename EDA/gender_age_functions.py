import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, kruskal

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


def gender_count_series_bar(gender_age_table, series_seat, title = 'Counts of Male and Female per Series'):

    if series_seat.lower() == 'series':
        gender_series_plot = gender_age_table.groupby(['Series Number', 'Gender']).size().unstack(fill_value=0)
        series = gender_series_plot.index
        x = np.arange(len(series))+1
        x_label = 'Series'
        x_range = (0.25, 20.75)
        y_range = (0, 5)
    
    if series_seat.lower() == 'seat':
        gender_series_plot = gender_age_table.groupby(['Seat', 'Gender']).size().unstack(fill_value=0)
        seat = gender_series_plot.index
        x = np.arange(len(seat))+1
        x_label = 'Seat'
        x_range = (0.5, 5.5)
        y_range = (0, 15)

    width = 0.4

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

    plt.xlabel(x_label, fontsize = 20)
    plt.ylabel('Count', fontsize = 20)
    plt.ylim(y_range)
    plt.xlim(x_range)
    plt.title(title, fontsize = 25)
    plt.xticks(x, fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.legend(fontsize = 18)
    plt.show()

def setting_age_bins(table):
    age_table = table.copy()
    age_bins = [20, 30, 40, 50, 60, 70]
    age_labels = ['20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69']
    age_table['Age_Ranges'] = pd.cut(age_table['Age_at_First_Air'], bins = age_bins, labels = age_labels, right = False)
    print(age_table)
    return(age_table)

def age_range_metrics(table):
    age_table = table.copy()
    age_ranges_count = age_table['Age_Ranges'].value_counts().reset_index()
    age_ranges_count.columns = ['Age_Ranges', 'Count']
    age_ranges_count['Percentage'] = (age_ranges_count['Count'] / age_ranges_count['Count'].sum()) * 100
    print(age_ranges_count)
    return(age_ranges_count)

def age_group_series(table):
    age_table = table.copy()
    age_series = age_table.groupby('Series Number')['Age_Ranges'].value_counts().reset_index()
    age_series = age_series.sort_values('Series Number', ascending = True)
    print(age_series)
    return(age_series)

def age_series_stacked_bar(table, series_seat, title):

    if series_seat.lower() == 'series':
        x_axis = "Series Number"
        x_label = "Series"
        text_loc_x = 0.05
        text_loc_y = 5.33
        y_ticks = [0, 1, 2, 3, 4, 5]
    
    if series_seat.lower() == 'seat':
        x_axis = "Seat"
        x_label = 'Seat'
        text_loc_x = -0.5
        text_loc_y = 21.4
        y_ticks = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    age_series_plot = table.pivot_table(index=x_axis, columns="Age_Ranges", values="count",
                aggfunc="sum", fill_value=0, observed=True).reset_index()
    
    print(age_series_plot)
    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.88, left = 0.08, right = 0.96) 
    ax = age_series_plot.plot(x=x_axis, kind='bar', stacked=True, width = 0.8, ax = ax)

    for c in ax.containers:
        labels = [f"{int(v.get_height())}"
                if np.isfinite(v.get_height()) and v.get_height() > 0 else '' for v in c]
        
        ax.bar_label(c, labels=labels, label_type='center', color = 'white', fontsize = 14)
    
    plt.text(text_loc_x, text_loc_y, 'Age Ranges:', fontsize = 14)

    ax.tick_params(axis='x', labelrotation=0)
    plt.xlabel(x_label, fontsize = 20)
    plt.ylabel("Count", fontsize = 20)
    plt.xticks(fontsize = 18)
    plt.yticks(y_ticks, fontsize = 18)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=5, fontsize=14, frameon=False)
    plt.title(title, pad=30, fontsize = 24)
    plt.show()


def merge_series_age_gender(series_table, gender_table, age_table):

    series_table = series_table.copy()
    gender_table = gender_table.copy() 
    age_table = age_table.copy()

    final_scores_age_gender = pd.merge(left = series_table, right = gender_table.drop('Series', axis = 1),
                                    on = 'Name', how = 'left')

    final_scores_age_gender = pd.merge(left = final_scores_age_gender, 
                                    right = age_table.drop(['Series Number', 'Age_at_First_Air'], axis = 1), 
                                    on = 'Name', how = 'left')

    print(final_scores_age_gender)
    return(final_scores_age_gender)

def seat_gender_metrics(datatable):
    datatable = datatable.copy()
    seat_gender_table = datatable[['Seat', 'Gender']]
    seat_gender_table['Seat'] = seat_gender_table['Seat'].str.replace('Seat ', '').astype(int)
    print(seat_gender_table)
    return(seat_gender_table)

def seat_age_metrics(datatable):
    datatable = datatable.copy()
    seat_age_table = datatable[['Seat', 'Age_Ranges']]
    seat_age_table['Seat'] = seat_age_table['Seat'].str.replace('Seat ', '').astype(int)
    seat_age_table = seat_age_table.groupby('Seat')['Age_Ranges'].value_counts().reset_index()
    print(seat_age_table)
    return(seat_age_table)


def chi2_test(data_table, values, index, columns, agg):
    
    contingency = pd.pivot_table(data_table, values=values, index=index, columns=columns, 
                                 aggfunc=agg, fill_value=0)
    
    chi2, pvalue, dof, expected = chi2_contingency(contingency)

    expected_table = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)

    print('Observed Table:\n', contingency)
    print()
    print('Expected Table:\n', expected_table)

    print(f"Chi-squared statistic: {chi2:.3f}")
    print(f"Degrees of freedom: {dof}")
    print(f"P-value: {pvalue:.6f}")
    
    print('/n/n')