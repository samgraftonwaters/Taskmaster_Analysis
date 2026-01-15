import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def count_scores(dataframe, score : int):

    """
    Counts the number of times each score (1 - 5) was given for each seat in each series.

    Parameters:
    -----------
        dataframe (DataFrame): dataframe with all scores per episode and task in all series
        score (int): Number of the score value to be counted

    Returns:
    --------
        DataFrame that has the score count for each seat during all episodes of each series
    
    """

    count_score = []

    for series in range(1, 21):

        data = pd.read_excel(dataframe, sheet_name = f'Series_{series}')
        cols = data.columns
        contestents = cols[2:7]

        #Counting number of times contestnts scored a score of 1 or 5 in each task
        scores = data[data['Task Number'] != f'Series {series} Grand Total'].reset_index(drop = True)
        scores = scores[contestents]
        count_scores = scores[scores == score].count(axis = 0)
        count_score.append(count_scores)

    count = pd.DataFrame(np.vstack(count_score), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'])

    series = []
    for i in range(20):
        series.append(f'S{count.index.values[i] + 1}')
    count['Series'] = series

    return(count)


def most_least_scores(count_scores, named_table, score : int, size : str):

    """
    Finds the contestents with the most and least number of ones and fives per series. Function merges the 
    named table with contestents the count table in the final stage.

    Parameters:
    ----------
        count_scores (DataFrame): table with total counts of each score (e.g. 1 - 5) for each seat
        name_table (DataFrame): contestent name table
        score (int): score for a task (e.g. 1 - 5)
        size (string): filter to determine if the most or least number of each score for each seat is selected. 
                    Options are "most" for most number; "leat" for least number
    
    Return:
    -------
        Returns a DataFrame with the most (if size = 'most') or least (if size = 'least') number of times
        each score was given for each seat per series.
    
    """

    most = []
    least = []
    
    for seat in range(1, 6):
        count = count_scores[['Series', f'Seat {seat}']]

        mostcounts = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
        mostcounts['Seat'] = f'Seat {seat}'
        most.append(mostcounts)

        leastcounts = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
        leastcounts['Seat'] = f'Seat {seat}'
        least.append(leastcounts)

    if size.lower() == 'most':
        most = pd.DataFrame(np.vstack(most), columns = ['Series', f'Most {str(score)}s', 'Seat'])

        most = pd.merge(left = most, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values(f'Most {str(score)}s', ascending = False).reset_index(drop = True)

        most['index'] = most.index.values + 1

        return(most)
    
    if size.lower() == 'least':
        least = pd.DataFrame(np.vstack(least), columns = ['Series', f'Least {str(score)}s', 'Seat'])

        least = pd.merge(left = least, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values(f'Least {str(score)}s', ascending = False).reset_index(drop = True)

        least['index'] = least.index.values + 1

        return(least)


def high_low_ep_scores(data_table, named_table, direction : str):

    """
    Finds the contestents with the highest or lowest episode scores in each series

    Parameters:
    ----------
        data_tabe (DataFrame): table with total scores for each episode.
        name_table (DataFrame): contestent name table
        directon (str): to select if the highest or lowest episode scores are returned. Two options - "highest"
                        or "lowest".
    
    Returns:
    --------
        dataframe with either the highest or lowest episode scores per contestent in all series. 
    """

    highest_ep_scores = []
    lowest_ep_scores = []
    for seat in range(1, 6):
        seat_ep_score = data_table[['Series', 'Episode', f'Seat {seat}']]

        highest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
        highest_ep['Seat'] = f'Seat {seat}'
        highest_ep_scores.append(highest_ep)

        lowest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
        lowest_ep['Seat'] = f'Seat {seat}'
        lowest_ep_scores.append(lowest_ep)

    if direction.lower() == 'highest':
        highest_ep_scores = pd.DataFrame(np.vstack(highest_ep_scores) , columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)
    
        highest_ep_scores = pd.merge(left = highest_ep_scores, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = False).reset_index(drop = True)

        highest_ep_scores['index'] = highest_ep_scores.index.values + 1

        return(highest_ep_scores)

    if direction.lower() == 'lowest':
        lowest_ep_scores = pd.DataFrame(np.vstack(lowest_ep_scores), columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)

        lowest_ep_scores = pd.merge(left = lowest_ep_scores, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = True).reset_index(drop = True)

        lowest_ep_scores['index'] = lowest_ep_scores.index.values + 1

        return(lowest_ep_scores)
    