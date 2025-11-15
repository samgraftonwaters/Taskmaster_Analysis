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

#Merging Tables
final_positions = TSE.total_score_positions_ordered
average_scores = TSE.average_tasks_positions_ordered.drop(['Seat', 'Position', 'Series'], axis = 1)

score_merged_table = pd.merge(final_positions, average_scores, on = 'Name', how = 'left')

total_eps = TSE.Total_per_episode.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'], axis = 1)
total_tasks = TSE.Total_per_task.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'], axis = 1)

tasks_episodes = pd.merge(total_eps, total_tasks, on = 'Series', how = 'left')

final_positions_dq_sort = pd.merge(dq_sort.drop('Series', axis = 1), score_merged_table, on = 'Name',  how = 'left')
final_positions_dq_sort = pd.merge(final_positions_dq_sort, tasks_episodes, on = 'Series',  how = 'left')
final_positions_dq_sort = final_positions_dq_sort.rename(columns = {'Score_x' : 'Total Score', 'Score_y' : 'Avg_Task_Score'})


print(final_positions_dq_sort.head())

sns.scatterplot(x = final_positions_dq_sort['DQ'], y = final_positions_dq_sort['Total Score'], 
                hue = final_positions_dq_sort['Position'], size = final_positions_dq_sort['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

sns.scatterplot(x = final_positions_dq_sort['DQ'], y = final_positions_dq_sort['Position'], 
                hue = final_positions_dq_sort['Total Score'], size = final_positions_dq_sort['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
plt.gca().invert_yaxis()
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Final Position', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

