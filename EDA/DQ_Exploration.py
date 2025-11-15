import pandas as pd
import numpy as np
import DQ_Functions as DQF
import Total_Scores_EDA as TSE

import matplotlib.pyplot as plt
import seaborn as sns

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

final_positions_dq_sort = pd.merge(dq_sort.drop('Series', axis = 1), final_positions, on = 'Name',  how = 'left')
print(final_positions_dq_sort)

sns.scatterplot(x = final_positions_dq_sort['DQ'], y = final_positions_dq_sort['Score'], 
                hue = final_positions_dq_sort['Position'], size = final_positions_dq_sort['Seat'])

plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()