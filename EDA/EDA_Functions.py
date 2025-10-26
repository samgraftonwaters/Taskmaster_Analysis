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

        total = total_score[contestents].reset_index(drop = True)

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

        total_per_number_eps = pd.DataFrame(total_score[contestents] / number_eps)

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

        total_per_number_tasks = pd.DataFrame(total_score[contestents] / number_tasks)
       
        total_per_number_tasks['Series'] = series
        total_per_number_tasks['Number of Tasks'] = number_tasks
        total_per_number_tasks.columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number Tasks']

        if include_col_names == False:

            # total_per_number_tasks.columns = range(total_per_number_tasks.shape[1])

            total_per_number_tasks = total_per_number_tasks.reset_index(drop = True).values

            return(total_per_number_tasks)
        
        else:
            return(total_per_number_tasks.reset_index(drop = True))