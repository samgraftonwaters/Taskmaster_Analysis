import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def most_least_scores(count_scores, named_table, value : str, size : str):

    """
    Finds the contestents with the most and least number of ones and fives per series. Function merges the 
    named table with contestents the count table in the final stage.

    Parameters:
    ----------
        count_scores (DataFrame): table with total counts of ones and fives for each seat
        name_table (DataFrame): contestent name table
        size (string): filter to determine if the most or least number is selected. Options are
                        "most" for most number; "leat" for least number
    
    Return:
    -------
        Returns a DataFrame with the most (if size = 'most') or least (if size = 'least') number of ones or fives
    
    """

    most = []
    least = []
    
    for seat in range(1, 6):
        count = count_scores[['Series', f'Seat {seat}']]

        mostcounts = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
        mostcounts['Seat'] = f'Seat {seat}'
        most.append(mostcounts)

        leastcount = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
        leastcount['Seat'] = f'Seat {seat}'
        least.append(leastcount)

    if size == 'most':
        most = pd.DataFrame(np.vstack(most), columns = ['Series', 'Most 1s', 'Seat'])

        most = pd.merge(left = most, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Most 1s', ascending = False).reset_index(drop = True)

        most['index'] = most.index.values + 1

        print(most)

        return(most)
    
    if size == 'least':
        least = pd.DataFrame(np.vstack(least), columns = ['Series', 'Least 1s', 'Seat'])

        least = pd.merge(left = least, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Least 1s', ascending = False).reset_index(drop = True)

        least['index'] = least.index.values + 1

        return(least)
    


    # most_ones = []
    # least_ones = []

    # most_fives = []
    # least_fives = []

    # for seat in range(1, 6):
    #     ones = count_one[['Series', f'Seat {seat}']]
    #     fives = count_five[['Series', f'Seat {seat}']]

    #     mostones = ones[ones[f'Seat {seat}'] == ones[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
    #     mostones['Seat'] = f'Seat {seat}'
    #     most_ones.append(mostones)
        
    #     leastones = ones[ones[f'Seat {seat}'] == ones[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
    #     leastones['Seat'] = f'Seat {seat}'
    #     least_ones.append(leastones)

    #     mostfives = fives[fives[f'Seat {seat}'] == fives[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
    #     mostfives['Seat'] = f'Seat {seat}'
    #     most_fives.append(mostfives)
        
    #     leastfives = fives[fives[f'Seat {seat}'] == fives[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
    #     leastfives['Seat'] = f'Seat {seat}'
    #     least_fives.append(leastfives)

    # most_ones = pd.DataFrame(np.vstack(most_ones), columns = ['Series', 'Most 1s', 'Seat'])
    # least_ones = pd.DataFrame(np.vstack(least_ones), columns = ['Series', 'Least 1s', 'Seat'])

    # most_ones = pd.merge(left = most_ones, right = named_series_table_reformatted, 
    #                             on = ['Series', 'Seat'], how = 'left').sort_values('Most 1s', ascending = False).reset_index(drop = True)

    # most_ones['index'] = most_ones.index.values + 1

    # least_ones = pd.merge(left = least_ones, right = named_series_table_reformatted, 
    #                             on = ['Series', 'Seat'], how = 'left').sort_values('Least 1s', ascending = False).reset_index(drop = True)

    # least_ones['index'] = least_ones.index.values + 1

    # most_fives = pd.DataFrame(np.vstack(most_fives), columns = ['Series', 'Most 5s', 'Seat'])
    # least_fives = pd.DataFrame(np.vstack(least_fives), columns = ['Series', 'Least 5s', 'Seat'])

    # most_fives = pd.merge(left = most_fives, right = named_series_table_reformatted, 
    #                             on = ['Series', 'Seat'], how = 'left').sort_values('Most 5s', ascending = False).reset_index(drop = True)

    # most_fives['index'] = most_fives.index.values + 1

    # least_fives = pd.merge(left = least_fives, right = named_series_table_reformatted, 
    #                             on = ['Series', 'Seat'], how = 'left').sort_values('Least 5s', ascending = False).reset_index(drop = True)

    # least_fives['index'] = least_fives.index.values + 1