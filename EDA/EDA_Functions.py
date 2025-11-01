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

    print(dataframe.info())
    print(dataframe.isna().sum())
    
    total_score = dataframe[dataframe['Task Number'].str.contains('Grand Total', na = False)]

    print(total_score)

    series = dataframe.loc[dataframe['Task Number'].str.contains('Grand Total', na = False)]['Series'].values

    if total == True:

        total = total_score[contestents].reset_index(drop = True).astype(int)

        total['Series'] = series

        total.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series']

        if include_col_names == False:

            # total.columns = range(total.shape[1])

            total = total.values

            return(total)

        else:

            return(total)

    if per_number_eps == True:

        number_eps = dataframe['Episode'].str.contains(r"Ep.*Total", regex=True).sum()

        print(f'{number_eps=}')

        total_per_number_eps = pd.DataFrame(round((total_score[contestents] / number_eps), 2))

        total_per_number_eps['Series'] = series
        total_per_number_eps['Number of Episodes'] = number_eps
        total_per_number_eps.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number of Episodes']

        if include_col_names == False:

            # total_per_number_eps.columns = range(total_per_number_eps.shape[1])

            total_per_number_eps = total_per_number_eps.reset_index(drop = True).values

            return(total_per_number_eps)
        
        else:
            return(total_per_number_eps.reset_index(drop = True))
    
    if per_number_tasks == True:

        number_tasks = (~dataframe['Episode'].str.contains('Total', case=False, na=False)).sum()

        print(f'{number_tasks=}')

        total_per_number_tasks = pd.DataFrame(round((total_score[contestents] / number_tasks), 2))
       
        total_per_number_tasks['Series'] = series
        total_per_number_tasks['Number of Tasks'] = number_tasks
        total_per_number_tasks.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number Tasks']

        if include_col_names == False:

            # total_per_number_tasks.columns = range(total_per_number_tasks.shape[1])

            total_per_number_tasks = total_per_number_tasks.reset_index(drop = True).values

            return(total_per_number_tasks)
        
        else:
            return(total_per_number_tasks.reset_index(drop = True))
        

def total_score_tables(table, extra_columns):

    new_cols = [f"Seat {i+1}" for i in range(5)]

    if len(extra_columns) == 1:

        new_cols.append(extra_columns[0])
    
    else:
        new_cols.append(extra_columns[0])
        new_cols.append(extra_columns[1])

    table = np.vstack(table)

    total_table = pd.DataFrame(table, columns=new_cols)

    print(total_table)

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

    print(max_named_table)
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

    print(min_named_table)
    return(min_named_table)