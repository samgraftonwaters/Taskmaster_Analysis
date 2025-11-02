import pandas as pd
import numpy as np

def get_data(filepath, filename, sheetname, number_tables = None):

    if number_tables == None:
        data = pd.read_excel(filepath + filename, sheet_name = sheetname)
        return(data)
    
    else:
        data = []
        for tables in range(1, number_tables):
            data_tabs = pd.read_excel(filepath + filename, sheet_name = f'Series_{tables}')
            data.append(data_tabs)
        return(data)

def total_scores(dataframe, total, per_number_eps, per_number_tasks, include_col_names = True):

    dataframe = pd.DataFrame(dataframe)
    cols = dataframe.columns
    contestents = cols[2:7]
    
    total_score = dataframe[dataframe['Task Number'].str.contains('Grand Total', na = False)]

    series = dataframe.loc[dataframe['Task Number'].str.contains('Grand Total', na = False)]['Series'].values

    if total == True:

        total = total_score[contestents].reset_index(drop = True).astype(int)

        total['Series'] = series

        total.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series']

        if include_col_names == False:

            total = total.values

            return(total)

        else:

            return(total)

    if per_number_eps == True:

        number_eps = dataframe['Episode'].str.contains(r"Ep.*Total", regex=True).sum()

        total_per_number_eps = pd.DataFrame(round((total_score[contestents] / number_eps), 2))

        total_per_number_eps['Series'] = series
        total_per_number_eps['Number of Episodes'] = number_eps
        total_per_number_eps.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number of Episodes']

        if include_col_names == False:

            total_per_number_eps = total_per_number_eps.reset_index(drop = True).values

            return(total_per_number_eps)
        
        else:
            return(total_per_number_eps.reset_index(drop = True))
    
    if per_number_tasks == True:

        number_tasks = (~dataframe['Episode'].str.contains('Total', case=False, na=False)).sum()

        total_per_number_tasks = pd.DataFrame(round((total_score[contestents] / number_tasks), 2))
       
        total_per_number_tasks['Series'] = series
        total_per_number_tasks['Number of Tasks'] = number_tasks
        total_per_number_tasks.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number Tasks']

        if include_col_names == False:

            total_per_number_tasks = total_per_number_tasks.reset_index(drop = True).values

            return(total_per_number_tasks)
        
        else:
            return(total_per_number_tasks.reset_index(drop = True))
        

def total_score_tables(table, extra_columns, drop_total=True):

    new_cols = [f"Seat {i+1}" for i in range(5)]

    if len(extra_columns) == 1:

        new_cols.append(extra_columns[0])
    
    else:
        new_cols.append(extra_columns[0])
        new_cols.append(extra_columns[1])

    table = np.vstack(table)

    total_table = pd.DataFrame(table, columns=new_cols)

    total_table.insert(5, 'Total', total_table[new_cols[0:5]].sum(axis = 1))

    if drop_total == True:
        total_table = total_table.drop('Total', axis = 1)

    return(total_table)


def find_highest_seat(value_table, name_table):

    value_table = pd.DataFrame(value_table)

    max_table = []
    
    for seat in range(1,6):

        maximum = max(value_table[f'Seat {seat}'])
        
        series_max = value_table.loc[value_table[f'Seat {seat}'] == maximum]['Series'].reset_index(drop = True).values[0]
        
        max_table.append([f'Seat {seat}', maximum, series_max])
    
    max_table = pd.DataFrame(max_table, columns = ['Seat Number', 'Max Score', 'Series'])

    names_max = []

    for seat in range(5):

        name_max = name_table[name_table['Series'] == max_table['Series'][seat]].reset_index(drop = True)
       
        names_max.append(name_max[[f'Seat Name {seat+1}', 'Series']].values[0])
    
    names_max = pd.DataFrame(names_max, columns = ['Name', 'Series Name'])

    max_named_table = pd.concat([max_table, names_max], axis = 1)

    max_named_table = max_named_table.drop('Series Name', axis = 1)

    return(max_named_table)


def find_lowest_seat(value_table, name_table):

    value_table = pd.DataFrame(value_table)

    min_table = []
    for seat in range(1,6):

        minimum = min(value_table[f'Seat {seat}'])

        series_min = value_table.loc[value_table[f'Seat {seat}'] == minimum]['Series'].reset_index(drop = True).values[0]

        min_table.append([f'Seat {seat}', minimum, series_min])

    min_table = pd.DataFrame(min_table, columns = ['Seat Number', 'Min Score', 'Series'])

    names_min = []

    for seat in range(5):

        name_min = name_table[name_table['Series'] == min_table['Series'][seat]].reset_index(drop = True)

        names_min.append(name_min[[f'Seat Name {seat+1}', 'Series']].values[0])
    
    names_min = pd.DataFrame(names_min, columns = ['Name', 'Series Name'])

    min_named_table = pd.concat([min_table, names_min], axis = 1)

    min_named_table = min_named_table.drop('Series Name', axis = 1)

    return(min_named_table)



def total_scores_all_series(total_scores_df, number_episodes_df, number_tasks_df):

    new_cols = [f"Seat {i+1}" for i in range(5)]

    seat_totals = []
    for seat in range(1, 6):
        total_scores = total_scores_df[f'Seat {seat}'].sum()

        seat_totals.append(total_scores)

    summed_total_per_episodes = [x / number_episodes_df['Number of Episodes'].sum() for x in seat_totals]
    summed_total_per_episodes = pd.DataFrame([summed_total_per_episodes]).round(2)
    summed_total_per_tasks = [x / number_tasks_df['Number of Tasks'].sum() for x in seat_totals]
    summed_total_per_tasks = pd.DataFrame([summed_total_per_tasks]).round(2)
    
    seat_totals = pd.DataFrame([seat_totals])
    
    summed_totals_table = pd.concat([seat_totals, summed_total_per_episodes, summed_total_per_tasks], axis = 0).reset_index(drop = True)
    summed_totals_table.columns = new_cols

    Numbers = pd.DataFrame([20, number_episodes_df['Number of Episodes'].sum(), number_tasks_df['Number of Tasks'].sum()], columns = ['Series_Episodes_Tasks'])
    summed_totals_table = pd.concat([summed_totals_table, Numbers], axis = 1)

    return(summed_totals_table)


def seat_winner_each_series(dataframe):
    dataframe = pd.DataFrame(dataframe)

    cols = dataframe.columns

    winning_seat_each_series = dataframe[cols[0:5]].idxmax(axis = 1)

    series = dataframe[cols[5]]

    winning_seat = pd.concat([series, winning_seat_each_series], axis = 1)
    winning_seat.columns = ['Series', 'Seat Winner']

    return(winning_seat)

def seat_loser_each_series(dataframe):
    dataframe = pd.DataFrame(dataframe)

    cols = dataframe.columns

    columns = dataframe[cols[0:5]].idxmin(axis = 1)

    series = dataframe[cols[5]]

    losing_seat = pd.concat([series, columns], axis = 1)
    losing_seat.columns = ['Series', 'Seat Loser']
    
    return(losing_seat)


def order_seats(score_table, name_table):

    cols = [f"Seat {i+1}" for i in range(5)]

    score_table = score_table.drop('Total', axis =1)
    score_cols = score_table.columns

    name_cols = name_table.columns

    # Get sorted column order for each row
    series_ranks = score_table[cols].apply(lambda row: row.sort_values().index.tolist(), axis = 1)
    print(series_ranks)

    series_ranks = pd.DataFrame([series_ranks.tolist()], columns=[f'order_{i+1}' for i in range(len(cols))])
    print(series_ranks)
    series_ranks.insert(0, 'Series', score_table['Series'])
    print(series_ranks)

    # Map column name to its corresponding _name column in df2
    name_map = {}
    for i, j in zip(score_cols,  name_cols):
        name_map.update({i : j})
        
    print(name_map)
    # # Create a new DataFrame of names in the same order
    # name_order_df = eries_ranks.apply(
    # lambda row: [name_table.loc[name_table['id'] == row['id'], name_map[c]].values[0] for c in row[1:]],
    # axis=1,
    # result_type='expand'
    # )
    # name_order_df.columns = [f'order_{i+1}_name' for i in range(len(cols))]
    # name_order_df.insert(0, 'id', score_table['id'])

    # # Combine both order and name order if desired
    # result = pd.concat([series_ranks, name_order_df.drop(columns='id')], axis=1)
    # print(result)

    

    