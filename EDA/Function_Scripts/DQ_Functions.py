import pandas as pd
import numpy as np
import Total_Scores_EDA as TSE
import matplotlib.pyplot as plt
import seaborn as sns

def count_DQ_all_contestents(file_path:str, table_name:str, number_series:int):

    """
    Creates a datatable that contains the number of disqualifications per contestent over all series

    Parameters:
    -----------
        file_path (str): filepath to the data folder
        table_name (str): name of file that contains all series data
        number_series (int): Number of series to iterate over. Default = 20

    Returns:
    --------
        dataframe with four columns - Contestent names ('Name'), number of disqualifications ('DQ'),
        series number ('Series') and seat number 'Seat'
    """
    
    count_dq = []

    for series in range(1, number_series+1):

        data = pd.read_excel(file_path + table_name, sheet_name = f'Series_{series}')
        cols = data.columns

        series_contestents = data[cols[4:9]]

        dq_count_values = series_contestents.eq('DQ').sum().values
        dq_count_index = series_contestents.eq('DQ').sum().index

        name_DQ = {}
        for i, j in zip(dq_count_index, dq_count_values):
            name_DQ.update({i : j})

        count_dq.append(name_DQ)

    dq_df_cols = [(name, score) for d in count_dq for name, score in d.items()]

    dq_df = pd.DataFrame(dq_df_cols, columns = ['Name', 'DQ'])
    dq_df["Series"] = [f"S{(i // 5) + 1}" for i in range(len(dq_df))]
    labels = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5']
    dq_df["Seat"] = [labels[i % 5] for i in dq_df.index]

    return(dq_df)

def dq_total_per_series(dataframe, number_series):

    """
    Creates a datatable for number of disqualifications in each series

    Parameters:
    -----------
        dataframe (dataframe): data table that contains the number of disqualifications for each
                                contestent and their respective series and seat
        number_series (int): number of series to iterate over

    Returns:
    --------
        dataframe with two columns - Series number ('Series') and number of disqualifications ('Total DQ')
    """

    total_dq = []
    for series in range(1, number_series + 1):

        series_df = dataframe[dataframe['Series'] == f'S{series}']

        series_totals = series_df['DQ'].sum()

        total_dq.append([f'S{series}', series_totals])

    total_dq_series = pd.DataFrame(total_dq, columns = ['Series', 'Total DQ'])

    return(total_dq_series)

def dq_total_each_seat(dataframe):

    """
    Creates a datatable for total number of disqualifications for each seat

    Parameters:
    -----------
        dataframe (dataframe): data table that contains the number of disqualifications for each
                                contestent and their respective series and seat

    Returns:
    --------
        dataframe with two columns - Seat number ('Seat') and number of disqualifications ('DQ')
    """

    seat_dq = dataframe.groupby(dataframe['DQ'] % 5).sum()
    
    dq_seat = pd.DataFrame(seat_dq['DQ']).reset_index(drop = True)

    dq_seat['Seat'] = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5']

    return(dq_seat)

def dq_series_bar(datatable):

    """
    Create bar plot for number of disqualifications in each series

    Parameters:
    -----------
        datatable (dataframe): data table that contains the series and number of disqualification columns 

    """

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.1, right = 0.95)

    plt.hlines(datatable['Total DQ'].mean(), -0.4, 19.4, linestyle = '--', lw = 3, color = 'black', 
            label = f'Average = {datatable['Total DQ'].mean()}')

    plt.bar(datatable['Series'], datatable['Total DQ'], color = 'red', alpha = 0.7, 
            edgecolor = 'black', lw = 2)

    for i in range(20):
        plt.text(i, datatable['Total DQ'][i]+0.8, 
                datatable['Total DQ'][i], ha='center', fontsize = 15, color = 'red')

    plt.legend(loc = 'upper left', fontsize = 16)
    plt.xlim(-0.5, 19.5)
    plt.ylim(0, 31)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.xlabel('Series', fontsize = 16)
    plt.ylabel('Number of Disqualifications', fontsize = 16)
    plt.title('Number of Disqualifications in each Series', fontsize = 20)
    plt.show()

def dq_seat_bar(datatable):

    """
    Create bar plot for number of disqualifications in each seats

    Parameters:
    -----------
        datatable (dataframe): data table that contains the seats and number of disqualification columns 

    """

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.05, top = 0.9, left = 0.1, right = 0.95)

    plt.hlines(datatable['DQ'].mean(), -0.5, 5.5, linestyle = '--', lw = 3, color = 'black',
            label = f'Average = {datatable['DQ'].mean()}')

    plt.bar(datatable['Seat'], datatable['DQ'], color = 'blue', alpha = 0.7, 
            edgecolor = 'black', lw = 2)

    for i in range(5):
        plt.text(i, datatable['DQ'][i]-3, 
                datatable['DQ'][i], ha='center', fontsize = 18, color = 'white')

    plt.legend(loc = 'upper left', fontsize = 16)
    plt.xlim(-0.5, 4.5)
    plt.ylim(0, 64)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.ylabel('Number of Disqualifications', fontsize = 16)
    plt.title('Number of Disqualifications in each Seat', fontsize = 20)
    plt.show()

def dq_contestent_count_bar(datatable):

    """
    Create bar plot for count of the number of disqualifications for each contestent

    Parameters:
    -----------
        datatable (dataframe): data table that contains the count for each distrinct number of 
        disqualificaitons for all contestents 

    """

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.1, right = 0.95)

    plt.bar(datatable['DQ'], datatable['Count'], color = 'dodgerblue', alpha = 0.7, 
            edgecolor = 'black', lw = 2)

    for i in datatable['DQ']:
        plt.text(i, datatable['Count'][i]+1, 
                datatable['Count'][i], ha='center', fontsize = 18, color = 'dodgerblue')

    plt.xlim(-0.5, 7.5)
    plt.ylim(0, 30)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.xlabel('Number of Disqualifications per Contestent', fontsize = 16)
    plt.ylabel('Count', fontsize = 16)
    plt.title('Count of Number of Disqualifications per Contestent', fontsize = 20)
    plt.show()




    


    