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

final_positions_dq['Missed Scores'] = (final_positions_dq['Avg_Task_Score'] * final_positions_dq['DQ']).astype(int)
final_positions_dq['Total Missed Scores'] = final_positions_dq['Missed Scores'] + final_positions_dq['Total Score']

# print(final_positions_dq.head())

missed_score_table = final_positions_dq[['Name', 'Series', 'Total Missed Scores']]

new_positions = []
for series in range(1, 21):

    series_df = missed_score_table[missed_score_table['Series'] == f'S{series}']

    series_df = series_df.sort_values('Total Missed Scores', ascending = False).reset_index(drop = True)

    series_df['New Position'] = [1, 2, 3, 4, 5]

    new_positions.append(series_df)

new_positions = pd.DataFrame(np.vstack(new_positions), columns = ['Name', 'Series', 'Total Missed Scores', 'New Position'])

final_positions_dq = pd.merge(final_positions_dq, new_positions.drop(['Series', 'Total Missed Scores'], axis = 1), on = 'Name', how = 'left')

final_positions_dq['Position Difference'] = final_positions_dq['Position'] - final_positions_dq['New Position']

# print(final_positions_dq.columns)

# print(final_positions_dq[final_positions_dq['Series'] == 'S1'][['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
#        'Position Difference']].head(30))

# sns.scatterplot(x = final_positions_dq['Avg_Task_Score'], y = final_positions_dq['Total Score'], 
#                 hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Total Score'], 
#                 hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Position'], 
#                 hue = final_positions_dq['Total Score'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
# plt.gca().invert_yaxis()
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Final Position', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

dq_change = final_positions_dq[(final_positions_dq['Position Difference'] != 0)]
                              # (final_positions_dq['Total Score'] != final_positions_dq['Total Missed Scores']))].reset_index(drop = True)
dq_change = dq_change[~dq_change['Name'].isin(['Frank Skinner', 'Romesh Ranganathan',
                                                      'Desiree Burch', 'Alan Davies'])].reset_index(drop = True)
# final_positions_dq['Position Difference'] = np.where(final_positions_dq['Total Score'] == final_positions_dq['Total Missed Scores'], 0,
#                                                      final_positions_dq['Position'] - final_positions_dq['New Position'])

dq_change_plus = dq_change[dq_change['Position Difference'] == 1]
dq_change_minus = dq_change[dq_change['Position Difference'] == -1]
#dq_change_minus['Total Score'] = dq_change_minus['Total Score']#.copy() * -1
#dq_change_minus['Total Missed Scores'] = dq_change_minus['Total Missed Scores']#.copy() * -1

series = dq_change_plus['Series'].unique()
y_values = np.arange(len(dq_change_plus['Series'].unique()))+1

print(dq_change[['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
       'Position Difference']].head(20))

# print(dq_change_plus[['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
#        'Position Difference']].head(20))


ax1_y_pos = [0.3, 0.71, 1.3, 1.71, 2.3, 2.71, 3.3, 3.71, 4.3, 4.71, 5.3, 5.71, 6.3, 6.71, 7.3, 7.71]
ax2_y_pos  = [0.78, 1.70, 2.62, 3.548, 4.46, 5.359, 6.3, 7.22]
ax2_x_pos = [1, 2, 3, 4, 5]

fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)
ax1 = fig.subplots()
ax2 = ax1.twinx()
ax3 = ax1.twiny()

ax1.barh(ax1_y_pos, dq_change['Total Missed Scores'], height = 0.35, color = 'red', lw = 1.5, edgecolor = 'black', alpha=0.7)
ax1.barh(ax1_y_pos, dq_change['Total Score'], height = 0.35, color = 'blue', lw = 1.5, edgecolor = 'black', alpha=0.7)
ax1.barh(ax1_y_pos, 50, color = 'white', height = 0.5)

ax2.set_ylim(ax1.get_ylim())
for y in ax2_y_pos:
    ax2.hlines(y, xmin=140, xmax=250, colors='gray', linestyles='--',linewidth=0.8)

ax3.set_ylim(ax1.get_ylim()) 
xmin, xmax = 1, 5
xgrid = np.arange(xmin, xmax+0.1, 1) 
ax3.vlines(xgrid, ymin=ax3.get_ylim()[0], ymax=ax3.get_ylim()[1], colors='gray', 
           linestyles='--', linewidth=0.8)

ax3.plot([dq_change['Position'][2:], dq_change['New Position'][2:]], [ax1_y_pos[2:], ax1_y_pos[2:]], '-', color = 'black', lw = 3)
ax3.plot([dq_change['Position'][0], dq_change['New Position'][0]], [ax1_y_pos[0], ax1_y_pos[0]], '-', color = 'black', lw = 3)

ax3.plot(dq_change_plus['Position'][1:], [1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3], 'o', markersize = 14, color = 'blue')
ax3.plot(dq_change_minus['Position'][1:], [1.7, 2.7, 3.7, 4.7, 5.7, 6.7, 7.7], 'o', markersize = 14, color = 'blue')
ax3.plot(dq_change_plus['New Position'][1:], [1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3], '^', markersize = 14, color = 'darkgreen')
ax3.plot(dq_change_minus['New Position'][1:], [1.7, 2.7, 3.7, 4.7, 5.7, 6.7, 7.7], 'v', markersize = 14, color = 'red')

ax3.plot(dq_change_plus['Position'][0], 0.3, 'o', markersize = 14, color = 'blue')
ax3.plot(dq_change_minus['Position'][1], 0.7, 'o', markersize = 14, color = 'blue')
ax3.plot(dq_change_plus['New Position'][0], 0.3, '^', markersize = 14, color = 'darkgreen')
ax3.plot(dq_change_minus['Position'][1], 0.7, 'o', markersize = 14, color = 'blue')
         
ax1.text(41, 8.5, '# DQ', fontsize = 14)
ax1.text(175, 8.55, 'Position:', fontsize = 16)

for y, value in zip(ax1_y_pos, dq_change['DQ']):
       ax1.text(45, y-0.1, str(value), fontsize = 14)

for y, score in zip(ax1_y_pos, dq_change['Total Missed Scores']):
     ax1.text(score+1,y-0.1, str(score), fontsize = 12, color = 'darkred')

for y, score in zip(ax1_y_pos, dq_change['Total Score']):
     ax1.text(score-10,y-0.1, str(score), fontsize = 12, color = 'white')

ax1.axvline(50, color='black', linewidth=1)
ax1.set_xlim(40, 230)
ax1.set_xticks([60, 100, 140, 180])
ax1.set_yticks(ticks = ax1_y_pos, labels = dq_change['Name'])

ax1.tick_params(axis='both', labelsize=14)
ax1.set_xlabel('Total Score', fontsize = 20)

ax2.set_ylim(0, 8)
ax2.set_yticks(ticks = ax2_y_pos, labels = dq_change['Series'].unique())
ax2.tick_params(axis='both', labelsize=14)
ax2.set_ylabel('Series', fontsize = 20)

ax3.tick_params(axis='both', labelsize=14)
ax3.set_xlim(-25, 6)
ax3.set_xticks(ax2_x_pos)

plt.show()


