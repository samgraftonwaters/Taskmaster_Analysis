import pandas as pd
import numpy as np
import EDA_Functions as EF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

series1 = EF.get_data(filepath = file_path, filename='Taskmaster_Series_Scores_Cleaned.xlsx', sheetname='Series_4', number_tables=None)

series1_total = EF.total_scores(dataframe = series1, total = True, per_number_eps = False, per_number_tasks = False, include_col_names = False)
series1_total_per_ep = EF.total_scores(dataframe = series1, total = False, per_number_eps = True, per_number_tasks = False, include_col_names = False)
series1_total_per_task = EF.total_scores(dataframe = series1, total = False, per_number_eps = False, per_number_tasks = True, include_col_names = False)

print(series1_total)
# print(series1_total_per_ep)
# print(series1_total_per_task)

Total_per_series = []
Total_per_episode = []
Total_per_task = []

for series in range(1, 21):

    data = pd.read_excel(file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx', sheet_name = f'Series_{series}')
    
    print(f'Series{series}')

    series_total = EF.total_scores(dataframe = data, total = True, per_number_eps = False, per_number_tasks = False, include_col_names = False)
    Total_per_series.append(series_total)

    series_total_per_ep = EF.total_scores(dataframe = data, total = False, per_number_eps = True, per_number_tasks = False, include_col_names = False)
    Total_per_episode.append(series_total_per_ep)

    series_total_per_task = EF.total_scores(dataframe = data, total = False, per_number_eps = False, per_number_tasks = True, include_col_names = False)
    Total_per_task.append(series_total_per_task)


print(Total_per_series)
print(Total_per_episode)
print(Total_per_task)

Total_per_series = EF.total_score_tables(table = Total_per_series, extra_columns=['Series'])
Total_per_episode = EF.total_score_tables(table = Total_per_episode, extra_columns=['Series', 'Number of Episodes'])
Total_per_task = EF.total_score_tables(table = Total_per_task, extra_columns=['Series', 'Number of Tasks'])

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
print(named_series_table.head())

EF.find_highest_lowest_seat(value_table = Total_per_series, name_table = named_series_table)
# EF.find_highest_lowest_seat(value_table = Total_per_episode, name_table = None)
# EF.find_highest_lowest_seat(value_table = Total_per_task, name_table = None)