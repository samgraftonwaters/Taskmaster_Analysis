import pandas as pd
import numpy as np

def get_data(filepath:str, filename:str, sheetname:str, number_tables:int = None):

    """
    Used to obtain the data for analysis, either calling one series at a time or multiple.

    Parameters:
    -----------
        filepath (string): path to the directory where the data is saved
        filename (string): name of the file that contains the data
        sheetname (list of strings): name of the sheet or sheets that contain the data
        number_tables (int): number of tables to be extracted from the data table. Note, 
                            this is taken in order of the series. i.e. if "number_tables" = 3,
                            series 1, 2, and 3 will be extracted.

    Returns:
    --------
        Dataframe(s) with the data to analyse.
    
    """

    if number_tables == None:
        data = pd.read_excel(filepath + filename, sheet_name = sheetname)
        return(data)
    
    else:
        data = []
        for tables in range(1, number_tables):
            data_tabs = pd.read_excel(filepath + filename, sheet_name = f'Series_{tables}')
            data.append(data_tabs)
        return(data)

def total_scores(dataframe, total:bool = True, per_number_eps:bool = False, 
                 per_number_tasks:bool = False, include_col_names:bool = True):

    """
    Calculates the total scores for a single series, and ccclulates the average per number of 
    episodes and number of tasks. One option can be taken at a time - e.g. only the totals or average
    per episodes are returned

    Parameters:
    -----------
        dataframe (dataframe): data table that is to be analysed
        total (bool): if True, then the total for each series will be calculated (default is True)
        per_number_eps (bool): if True, then it averages the total for each contestent based on the 
                                number of episodes in the series (default = False)
        per_number_tasks (bool): : if True, then it averages the total for each contestent based on the 
                                number of tasks in the series (default = False)
        include_col_names (bool): if True, then the final output will contain the column headings. (Default = True)
                                As this function returns the values for one series at a time, setting this
                                to False means that multiple outputs can be merged without every other row
                                containing the column names

    Returns:
    --------
        Values for each chair (and the respective Series) for a single series. Boolean option determines
        what output is given - total, average per episodes or average per number of tasks
    
    """

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
        
def total_score_tables(table, extra_columns:list | str, drop_total=True):

    """
    Cleans and structures the total and average total tables obtained from the function "total_scores()"

    Parameters:
    ---------
        table (array): series total scores array/table to be combined
        extra_column (list of strings): Adds additional columns such as "number of tasks", depending on 
                                        the initial table values
        drop_total (boolean): if True, the "Total" column, automatically constructed, is dropped from the
                            final dataframe output
    
    Returns:
    --------
        Structed and combined dataframe table for all series totals.
    """

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

    """
    Function to find the highest scores and contestents for each seat.

    Parameters:
    -----------
        value_table (data): table that contains all scores for each seat over all searies
        name_table (data): table that contains the contestents and their respective seats for each series
    
    Returns:
    --------
        data table containing the highest score, series and contestent name for each seat
    """

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

    """
    Function to find the lowest scores and contestents for each seat.

    Parameters:
    -----------
        value_table (data): table that contains all scores for each seat over all searies
        name_table (data): table that contains the contestents and their respective seats for each series
    
    Returns:
    --------
        data table containing the lowest score, series and contestent name for each seat
    """
        
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

    """
    Calculates the total scores for all series summed, and the average per number of episodes or tasks
    in one output table.

    Parameters:
    ----------
        total_scores_df (data): data table containing all total scores for each seat and series
        number_episodes_df (data): data table containing all total scores per number of epdisodes
                                for each seat and series
        number_tasks_df (data): data table containing all total scores per number of tasks
                                for each seat and series

    Returns:
    --------
        Three row table (excluding column names) with the total and averages for all series for each seat.

    """

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

    summed_totals_table['Averages'] = round(summed_totals_table[summed_totals_table.columns[0:5]].sum(axis = 1)/5, 2)

    return(summed_totals_table)


def seat_winner_each_series(dataframe):

    """
    Obtains the winning seat for each season

    Parameters:
    -----------
        dataframe (data): a table that contains all scores for each seat over all series

    Returns:
    --------
        Two column table containing the series and the seat winner 
    """
    
    dataframe = pd.DataFrame(dataframe)

    cols = dataframe.columns

    winning_seat_each_series = dataframe[cols[0:5]].idxmax(axis = 1)

    series = dataframe[cols[6]]

    winning_seat = pd.concat([series, winning_seat_each_series], axis = 1)
    winning_seat.columns = ['Series', 'Seat Winner']

    return(winning_seat)

def seat_loser_each_series(dataframe):

    """
    Obtains the losing seat for each season

    Parameters:
    -----------
        dataframe (data): a table that contains all scores for each seat over all series

    Returns:
    --------
        Two column table containing the series and the seat loser
    """

    dataframe = pd.DataFrame(dataframe)

    cols = dataframe.columns

    columns = dataframe[cols[0:5]].idxmin(axis = 1)

    series = dataframe[cols[6]]

    losing_seat = pd.concat([series, columns], axis = 1)
    losing_seat.columns = ['Series', 'Seat Loser']
    
    return(losing_seat)


def final_score_seat_positions(score_table, name_table, contain_summed_total = True):

    """
    Obtains a table that contains the seat order and therefore the contestent order for each series, 
    loser to winner

    Parameters:
    -----------
        scoree_table (data): table that contains all scores for each seat over all searies
        name_table (data): table that contains the contestents and their respective seats for each series
        contain_summed_total (boolean): If true, the score table contains a "Total" column and must be
                                        stated to be removed by the function. Default = True.

    Returns:
    --------
        Table with series orders from loser to winner based on seats and contestent names    
    """

    cols = [f"Seat {i+1}" for i in range(5)]

    if contain_summed_total == True:
        score_table = score_table.drop('Total', axis =1)
    
    score_cols = score_table.columns

    name_cols = name_table.columns

    # Get sorted column order for each row
    series_ordered = score_table[cols].apply(lambda row: row.sort_values(ascending = True).index.tolist(), axis = 1)
    series_ranks = pd.DataFrame(series_ordered.tolist(), columns=[f'order_{i+1}' for i in range(len(cols))])

    series_ranks.insert(0, 'Series', score_table['Series'])
    # Map column name to its corresponding _name column in df2
    name_map = {}
    for i, j in zip(score_cols,  name_cols):
        name_map.update({i : j})

    # # Create a new DataFrame of names in the same order
    name_order_df = series_ranks.apply(
        lambda row: [name_table.loc[name_table['Series'] == row['Series'], name_map[c]]
                     .values[0] for c in row[1:]], axis=1, result_type='expand'
    )
    name_order_df.columns = [f'order_{i+1}_name' for i in range(len(cols))]
    name_order_df.insert(0, 'Series', score_table['Series'])

    ordered_vals = (
        score_table[cols].apply(lambda row: row.sort_values().tolist(), axis=1)
        .apply(pd.Series).rename(columns=lambda i: f'value_{i+1}')
)
    # # Combine both order and name order if desired
    result = pd.concat([series_ranks, name_order_df.drop(columns='Series')], axis=1)

    result = pd.concat([result, ordered_vals], axis=1)

    result.columns = ['Series', 'Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                      'Second Place Seat', 'First Place Seat', 'Fifth Place Name', 'Fourth Place Name', 
                      'Third Place Name', 'Second Place Name', 'First Place Name', 'Fifth Place Score', 
                      'Fourth Place Score', 'Third Place Score', 'Second Place Score',
                      'First Place Score']

    return(result)

def ordering_final_scores_positions(dataframe, series_col:str, name_col:str, score_col:str, seat_col:str,
                               position:int, order:bool = True):

    """
    Combines the contestent name, total scores and series from the ordered table 
    for each series (1st to 5th), to then be used for plotting the total scores for each winner, loser,
    and those inbetween.

    Parameters:
    ----------
        dataframe (dataframe): dataframe created in function final_score_seat_orders(), which obtains 
                             series' first to fifth places
        series_col (string): name of the column that contains the series
        nam_col (string): column name that contains the names of all contestents finishing in the the
                        position of interest - e.g first place
        score_col (string): column name of the contestents final score
        seat_col (string): column containing the seat of each contestent
        position (integer): Position of contestent for their respective series. e.g. winner position = 1,
                            loser, position = 5
        order (boolean): if true, this will order the score column in ascending order, else the scores
                        will be in order of Series number. Default = True.

    Returns:
    --------
        dataframe with the above columns combined and ordered in ascending order (if set to True)
        based on the score. The column names are updated to 'Series', 'Name', 'Score' and 'Posiion'.
    """
    
    final_position = pd.concat([dataframe[series_col], dataframe[name_col], dataframe[score_col], dataframe[seat_col]], axis = 1)

    final_position.columns = ['Series', 'Name', 'Score', 'Seat']

    final_position['Position'] = position

    if order == True:

        final_position = final_position.sort_values(by = 'Score', ascending = True).reset_index(drop = True)

    return(final_position)
    

def ordering_final_scores_all_positions(datafame, series_col:list, name_cols:list, score_cols:list, 
                               seat_cols:list, positions:int, order_col:str, order:bool = True):

    """
    Combines the contestent name, total scores and series from the ordered table 
    for each series (1st to 5th), before concatonating all position tables into one.

    Parameters:
    ----------
        dataframe (dataframe): dataframe created in function final_score_seat_orders(), which obtains 
                             series' first to fifth places
        series_cols (list): name of the column that contains the series
        nam_cols (list): column name that contains the names of all contestents finishing in the the
                        position of interest - e.g first place
        score_cols (list): column name of the contestents final score
        seat_cols (list): column name with all seat numbers
        positions (integer): Position of contestent for their respective series. e.g. winner position = 1,
                            loser, position = 5
        order (boolean): if true, this will order the score column in ascending order, else the scores
                        will be in order of Series number. Default = True.

    Returns:
    --------
        dataframe with the all position tables combined (each in ascending order - if set to True - not the
        final table based on the score. The column names are updated to 'Series', 'Name', 'Score' and 'Position'.
    """

    positions_full_table = []

    for col in range(len(name_cols)):
        
        final_position = pd.concat([datafame[series_col], datafame[name_cols[col]], 
                                   datafame[score_cols[col]], datafame[seat_cols[col]]], axis = 1)

        final_position.columns = ['Series', 'Name', 'Score', 'Seat']

        final_position['Position'] = positions[col]

        if order == True:

            final_position = final_position.sort_values(by = order_col, ascending = True).reset_index(drop = True)
        
        positions_full_table.append(final_position)

    final_positions_full_table = pd.concat([positions_full_table[0], positions_full_table[1], 
                                           positions_full_table[2], positions_full_table[3],
                                           positions_full_table[4]], axis = 0)

    return(final_positions_full_table)
    

