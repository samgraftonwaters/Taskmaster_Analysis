import pandas as pd
import numpy as np
import Cleaning_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'


series1 = CF.get_data(filepath = file_path, filename='Taskmaster_Series_Scores_Cleaned.xlsx', sheetname='Series_1', number_tables=None)

# CF.clean_numerical(file_path = file_path, file_name = 'Taskmaster_Series_Scores', 
#                 sheet_name = 'Series', number_sheets = 20, output_filename = 'Taskmaster_Series_Scores_Cleaned')


series1_total = CF.total_scores(dataframe = series1, total = True, per_number_eps = False, per_number_tasks = False)
series1_total_per_ep = CF.total_scores(dataframe = series1, total = False, per_number_eps = True, per_number_tasks = False)
series1_total_per_task = CF.total_scores(dataframe = series1, total = False, per_number_eps = False, per_number_tasks = True)

print(series1_total)
print(series1_total_per_ep[0])
print(series1_total_per_task[1])

total_per_ep = series1_total_per_ep[0]

total_per_ep['Number of eps'] = series1_total_per_ep[1]

print(total_per_ep)