import pandas as pd
import numpy as np
from Function_Scripts import DQ_Functions as DQF
# import Total_Scores_EDA as TSE

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

number_of_series = 21

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
series_tables = file_path + 'Taskmaster_Series_Scores.xlsx'

dq_table = DQF.count_DQ_all_contestents(file_path = file_path, 
                                        table_name = 'Taskmaster_Series_Scores.xlsx', 
                                        number_series = 21)

#Bar charts for number of DQ per series and seats
dq_sort = dq_table.sort_values(by = 'DQ', ascending=False).reset_index(drop = True)

total_dq_series = DQF.dq_total_per_series(dataframe = dq_table, number_series = 21)

total_seat_dq = DQF.dq_total_each_seat(dataframe = dq_table)

#Merging Tables
final_positions = pd.read_csv(output_path + 'Total Final Scores and Positions.csv') 
average_scores = pd.read_csv(output_path + 'Avg Task Scores and Positions.csv')
average_scores = average_scores.drop(['Seat', 'Position', 'Series'], axis = 1)

score_merged_table = pd.merge(final_positions, average_scores, on = 'Name', how = 'left')

total_eps = pd.read_csv(output_path + 'Total Scores per Number of Episodes.csv')
total_tasks = pd.read_csv(output_path + 'Total Scores per Number of Tasks.csv')

total_eps = total_eps.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'], axis = 1)
total_tasks = total_tasks.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'], axis = 1)

tasks_episodes = pd.merge(total_eps, total_tasks, on = 'Series', how = 'left')

final_positions_dq = pd.merge(dq_table.drop(['Series', 'Seat'], axis = 1), score_merged_table, on = 'Name',  how = 'left')
final_positions_dq = pd.merge(final_positions_dq, tasks_episodes, on = 'Series',  how = 'left')
final_positions_dq = final_positions_dq.rename(columns = {'Score_x' : 'Total Score', 'Score_y' : 'Avg_Task_Score'})

final_positions_dq['Missed Scores'] = round((final_positions_dq['Avg_Task_Score'] * final_positions_dq['DQ']),0)
final_positions_dq['Total Missed Scores'] = final_positions_dq['Missed Scores'] + final_positions_dq['Total Score']

print(final_positions_dq)#.astype(int)

number_dq_ordered = final_positions_dq[['Name', 'DQ', 'Series', 'Total Score', 'Seat', 'Position']].sort_values('DQ', ascending = False)
count_dq = number_dq_ordered['DQ'].value_counts().reset_index()
count_dq.columns = ['DQ', 'Count']
count_dq = count_dq.sort_values(by = 'DQ', ascending=True).reset_index(drop = True)

missed_score_table = final_positions_dq[['Name', 'Series', 'Total Missed Scores']]

#Getting new positions
new_positions = []
for series in range(1, number_of_series + 1):

    series_df = missed_score_table[missed_score_table['Series'] == f'S{series}']

    series_df = series_df.sort_values('Total Missed Scores', ascending = False).reset_index(drop = True)

    series_df['New Position'] = [1, 2, 3, 4, 5]

    new_positions.append(series_df)

new_positions = pd.DataFrame(np.vstack(new_positions), columns = ['Name', 'Series', 'Total Missed Scores', 'New Position'])

final_positions_dq = pd.merge(final_positions_dq, new_positions.drop(['Series', 'Total Missed Scores'], axis = 1), on = 'Name', how = 'left')

final_positions_dq['Position Difference'] = final_positions_dq['Position'] - final_positions_dq['New Position']

print(final_positions_dq)

#Filtering table to remove rows where no change in position
dq_change = final_positions_dq[(final_positions_dq['Position Difference'] != 0)].reset_index(drop = True)

dq_change = dq_change[dq_change['Series'] != 'S21']
print(dq_change)

dq_change = dq_change[~dq_change['Name'].isin(['Frank Skinner', 'Romesh Ranganathan',
                                                      'Desiree Burch', 'Alan Davies'])].reset_index(drop = True)

dq_change_plus = dq_change[(dq_change['Position Difference'] == 1) | (dq_change['Position Difference'] == 2)| (dq_change['Position Difference'] == 3)]
dq_change_minus = dq_change[(dq_change['Position Difference'] == -1) | (dq_change['Position Difference'] == -2)| (dq_change['Position Difference'] == -3)]


dq_table.to_csv(output_path + 'DQ_Table.csv', sep = ',', index = False, encoding="utf-8")
dq_change.to_csv(output_path + 'DQ_position_changes.csv', sep = ',', index = False, encoding="utf-8")
final_positions_dq.to_csv(output_path + 'DQ_All_Contestents.csv', sep = ',', index = False, encoding="utf-8")

#####
#Plots
######

DQF.dq_series_bar(datatable = total_dq_series[total_dq_series['Series'] != 'S21'])

DQF.dq_seat_bar(datatable = total_seat_dq)

DQF.dq_contestent_count_bar(count_dq)

print(len(dq_change))
# ax1_y_pos = 
print([(i // 2) + (0.15 if i % 2 == 0 else 0.6) for i in range(len(dq_change))])
ax1_y_pos = [0.15, 0.6, 1.15, 1.6, 2.15, 2.6, 3.15, 3.6, 4.15, 4.6, 5.15, 5.6, 6.15, 6.6, 7.15, 7.6, 8.15, 8.6, 9.15, 9.6, 10.05]
ax1_y_pos_up = [0.6, 1.6, 2.6, 3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 9.6, 10.05]
ax1_y_pos_down = [0.15, 1.15, 2.15, 3.15, 4.15, 5.15, 6.15, 7.15, 8.15, 9.15]
print([0.76 + i * 0.91 for i in range(int(len(dq_change)/2))])
print([(ax1_y_pos[i] + ax1_y_pos[i+1]) / 2  for i in range(0, len(ax1_y_pos) - 3, 2)] + [sum(ax1_y_pos[-3:]) / 3])

ax2_y_pos = [0.6, 1.22, 1.83, 2.43, 3.05, 3.67, 4.28, 4.88, 5.5, 6.27] #[0.76, 1.67, 2.58, 3.49, 4.4, 5.31, 6.22, 7.13, 8.04, 8.95]
ax2_x_pos = [1, 2, 3, 4, 5]

fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)
ax1 = fig.subplots()
ax2 = ax1.twinx()
ax3 = ax1.twiny()

ax2.set_ylim(ax1.get_ylim())
for y in ax2_y_pos:
    ax2.hlines(y, xmin=80, xmax=250, colors='lightgray', linestyles='--', linewidth=0.8)

ax1.barh(ax1_y_pos, dq_change['Total Missed Scores'], height = 0.35, color = 'blue', lw = 1.5, edgecolor = 'black', alpha=0.7)
ax1.barh(ax1_y_pos, dq_change['Total Score'], height = 0.35, color = 'red', lw = 1.5, edgecolor = 'black', alpha=0.7)
ax1.barh(ax1_y_pos, 50, color = 'white', height = 0.5)
ax3.plot([dq_change['Position'], dq_change['New Position']], [ax1_y_pos, ax1_y_pos], '-', color = 'black', lw = 3)

ax3.set_ylim(ax1.get_ylim()) 
xmin, xmax = 1, 5
xgrid = np.arange(xmin, xmax+0.1, 1) 
ax3.vlines(xgrid, ymin=ax3.get_ylim()[0], ymax=ax3.get_ylim()[1],
          colors='lightgray', linestyles='--', linewidth=0.8)

ax3.plot(dq_change_plus['Position'], ax1_y_pos_up, 
         'o', markersize = 12, color = 'blue')
ax3.plot(dq_change_minus['Position'], ax1_y_pos_down, 
         'o', markersize = 12, color = 'blue')

ax3.plot(dq_change_plus['New Position'], ax1_y_pos_up, 
         '^', markersize = 12, color = 'darkgreen')
ax3.plot(dq_change_minus['New Position'], ax1_y_pos_down, 
         'v', markersize = 12, color = 'darkred')

ax1.text(42, (int(len(dq_change)/2) + 1.1), '# DQ', fontsize = 16)
ax1.text(175, (int(len(dq_change)/2) + 1.1), 'Position:', fontsize = 16)

for y, value in zip(ax1_y_pos, dq_change['DQ']):
       ax1.text(45, y-0.1, str(value), fontsize = 14)

for y, score in zip(ax1_y_pos, dq_change['Total Missed Scores']):
     ax1.text(score+1,y-0.1, str(score), fontsize = 12, color = 'darkblue')

for y, score in zip(ax1_y_pos, dq_change['Total Score']):
     ax1.text(score-10,y-0.1, str(score), fontsize = 12, color = 'white')

ax1.axvline(50, color='black', linewidth=1)
ax1.set_xlim(40, 230)
ax1.set_xticks([60, 100, 140, 180])
ax1.set_yticks(ticks = ax1_y_pos, labels = dq_change['Name'])
ax1.tick_params(axis='both', labelsize=14)
ax1.set_xlabel('Total Score', fontsize = 20)

ax2.set_ylim(0, 7)
ax2.set_yticks(ticks = ax2_y_pos, labels = dq_change['Series'].unique())
ax2.tick_params(axis='both', labelsize=14)
ax2.set_ylabel('Series', fontsize = 20)

ax3.tick_params(axis='both', labelsize=14)
ax3.set_xlim(-25, 6)
ax3.set_xticks(ax2_x_pos)

plt.show()