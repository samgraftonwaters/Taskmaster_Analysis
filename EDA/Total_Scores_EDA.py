import pandas as pd
import numpy as np
import EDA_Functions as EF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

series1 = EF.get_data(filepath = file_path, filename='Taskmaster_Series_Scores_Cleaned.xlsx', sheetname='Series_1', number_tables=None)

series1_total = EF.total_scores(dataframe = series1, total = True, per_number_eps = False, per_number_tasks = False)
series1_total_per_ep = EF.total_scores(dataframe = series1, total = False, per_number_eps = True, per_number_tasks = False)
series1_total_per_task = EF.total_scores(dataframe = series1, total = False, per_number_eps = False, per_number_tasks = True)

print(series1_total)
print(series1_total_per_ep)
print(series1_total_per_task)


