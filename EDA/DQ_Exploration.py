import pandas as pd
import numpy as np
import DQ_Functions as DQF
import Total_Scores_EDA as TSE

import matplotlib.pyplot as plt
import seaborn as sns

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

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

final_positions_dq = pd.merge(dq_table.drop('Series', axis = 1), score_merged_table, on = 'Name',  how = 'left')
final_positions_dq = pd.merge(final_positions_dq, tasks_episodes, on = 'Series',  how = 'left')
final_positions_dq = final_positions_dq.rename(columns = {'Score_x' : 'Total Score', 'Score_y' : 'Avg_Task_Score'})



final_positions_dq['Missed Scores'] = final_positions_dq['Avg_Task_Score'] * final_positions_dq['DQ']
final_positions_dq['Total Missed Scores'] = final_positions_dq['Missed Scores'] + final_positions_dq['Total Score']

print(final_positions_dq.head())

missed_score_table = final_positions_dq[['Name', 'Series', 'Total Missed Scores']]

new_positions = []
for series in range(1, 21):

    series_df = missed_score_table[missed_score_table['Series'] == f'S{series}']

    series_df = series_df.sort_values('Total Missed Scores', ascending = False).reset_index(drop = True)

    series_df['New Position'] = [1, 2, 3, 4, 5]

    new_positions.append(series_df)

new_positions = pd.DataFrame(np.vstack(new_positions), columns = ['Name', 'Series', 'Total Missed Scores', 'New Position'])

print(new_positions)

final_positions_dq = pd.merge(final_positions_dq, new_positions.drop(['Series', 'Total Missed Scores'], axis = 1), on = 'Name', how = 'left')

final_positions_dq['Position Difference'] = final_positions_dq['New Position'] - final_positions_dq['Position']
print(final_positions_dq.columns)

sns.scatterplot(x = final_positions_dq['Avg_Task_Score'], y = final_positions_dq['Total Score'], 
                hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Total Score'], 
                hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Position'], 
                hue = final_positions_dq['Total Score'], size = final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
plt.gca().invert_yaxis()
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Final Position', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

for seat, series, pos_diff, colour in zip(final_positions_dq['Seat'], final_positions_dq['Series'],
                                final_positions_dq['Position Difference'], colours):
    print(seat)
    plt.plot(series, pos_diff, '-o')
plt.show()
