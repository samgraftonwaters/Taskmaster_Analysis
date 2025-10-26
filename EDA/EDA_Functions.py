import pandas as pd
import numpy as np

def total_scores(dataframe, total, per_number_eps, per_number_tasks):

    dataframe = pd.DataFrame(dataframe)
    cols = dataframe.columns
    contestents = cols[2:7]
    
    total_score = dataframe[dataframe['Task Number'].str.contains('Grand Total')]

    if total == True:

        total = total_score[contestents].reset_index(drop = True)

        return(total)

    if per_number_eps == True:

        number_eps = dataframe['Episode'].str.contains(r"Ep.*Total", regex=True).sum()

        print(f'{number_eps=}')

        total_per_number_eps = pd.DataFrame(total_score[contestents] / number_eps)

        return(total_per_number_eps.reset_index(drop = True), number_eps)
    
    if per_number_tasks == True:

        number_tasks = (~dataframe['Episode'].str.contains('Total', case=False, na=False)).sum()

        print(f'{number_tasks=}')

        total_per_number_tasks = pd.DataFrame(total_score[contestents] / number_tasks)

        return(total_per_number_tasks.reset_index(drop = True), number_tasks)