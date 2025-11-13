import pandas as pd
import numpy as np
import DQ_Functions as DQF
import Total_Scores_EDA as TSE

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
series_tables = file_path + 'Taskmaster_Series_Scores.xlsx'

dq_table = DQF.count_DQ_all_contestents(file_path = file_path, 
                                        table_name = 'Taskmaster_Series_Scores.xlsx', 
                                        number_series = 20)

print(dq_table.head())

dq_sort = dq_table.sort_values(by = 'DQ', ascending=False).reset_index(drop = True)
print(dq_sort.head())
print(len(dq_sort))

final_positions = TSE.total_score_positions_ordered

print(final_positions)

final_positions_dq_sort = pd.merge(dq_sort, final_positions, on = 'Name',  how = 'left')
print(final_positions_dq_sort)
# for i in range(8):
#     print(i)
#     print(dq_sort[dq_sort['DQ'] == i])
#     print(len(dq_sort[dq_sort['DQ'] == i]))
#     print()
