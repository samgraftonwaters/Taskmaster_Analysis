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

print(final_positions_dq.columns)

print(final_positions_dq[final_positions_dq['Series'] == 'S1'][['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
       'Position Difference']].head(30))

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

dq_change = final_positions_dq[(final_positions_dq['Position Difference'] != 0)]
                              # (final_positions_dq['Total Score'] != final_positions_dq['Total Missed Scores']))].reset_index(drop = True)
dq_change = dq_change[~dq_change['Name'].isin(['Frank Skinner', 'Romesh Ranganathan',
                                                      'Desiree Burch', 'Alan Davies'])].reset_index(drop = True)
# final_positions_dq['Position Difference'] = np.where(final_positions_dq['Total Score'] == final_positions_dq['Total Missed Scores'], 0,
#                                                      final_positions_dq['Position'] - final_positions_dq['New Position'])

dq_change_plus = dq_change[dq_change['Position Difference'] == 1]
dq_change_minus = dq_change[dq_change['Position Difference'] == -1]
dq_change_minus['Total Score'] = dq_change_minus['Total Score'].copy() * -1
dq_change_minus['Total Missed Scores'] = dq_change_minus['Total Missed Scores'].copy() * -1

series = dq_change_plus['Series'].unique()
y_values = np.arange(len(dq_change_plus['Series'].unique()))+1

print(dq_change[['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
       'Position Difference']].head(20))

fig = plt.figure()
ax1 = fig.subplots()
ax2 = ax1.twiny()

ax1.barh(y_values-0.2, dq_change_plus['Total Missed Scores'], height = 0.4, color = 'white', edgecolor = 'blue')
ax1.barh(y_values+0.2, dq_change_plus['Total Score'], height = 0.4, color = 'white', edgecolor = 'green')

ax1.barh(y_values-0.2, dq_change_minus['Total Missed Scores'], height = 0.4, color = 'white', edgecolor = 'red')
ax1.barh(y_values+0.2, dq_change_minus['Total Score'], height = 0.4, color = 'white', edgecolor = 'darkorange')


ax1.vlines(x=dq_change_plus['Total Score'], ymin=y_values - 0, ymax=y_values +0.4, linewidth=3, color = 'blue')
ax1.vlines(x=dq_change_plus['Total Missed Scores'], ymin=y_values - 0.4, ymax=y_values +0, linewidth=3, color = 'green')

ax1.vlines(x=dq_change_minus['Total Score'], ymin=y_values - 0, ymax=y_values +0.4, linewidth=3, color = 'red')
ax1.vlines(x=dq_change_minus['Total Missed Scores'], ymin=y_values - 0.4, ymax=y_values +0, linewidth=3, color = 'darkorange')

for (y, name_plus, score_plus, missed_score_plus, 
              name_minus, score_minus, missed_score_minus) in zip(y_values, dq_change_plus['Name'], dq_change_plus['Total Score'],
                                                                  dq_change_plus['Total Missed Scores'], dq_change_minus['Name'], 
                                                                  dq_change_minus['Total Score'], dq_change_minus['Total Missed Scores']):
    print(name_plus)
    print(name_minus)
    
#     ax1.text(score_plus-100, y-0.2, name_plus, fontsize = 12, color = 'blue')
#     ax1.text(score_minus+100, y-0.2, name_minus, fontsize = 12, color = 'red')
    ax1.text(50, y-0.1, name_plus, fontsize = 14, color = 'blue')
    ax1.text(-120, y-0.1, name_minus, fontsize = 14, color = 'red')

    ax1.text(score_plus+2, y+0.15, str(round(score_plus,2)), fontsize = 14, color = 'blue')
    ax1.text(missed_score_plus+2, y-0.3, str(missed_score_plus), fontsize = 14, color = 'green')

    ax1.text(score_minus-45, y+0.2, str(round(score_minus,2)), fontsize = 14, color = 'red')
    ax1.text(missed_score_minus-45, y-0.3, str(missed_score_minus), fontsize = 14, color = 'darkorange')


ax2.plot(dq_change_plus['Position Difference'], y_values, marker = 'o', markersize = 15, color = 'darkgreen', linestyle='')
ax2.plot(dq_change_minus['Position Difference'], y_values, marker = 'o', markersize = 15, color = 'darkred', linestyle='')

# ax1.invert_yaxis()
# ax2.invert_yaxis()

ax1.tick_params(axis='x', labelsize=14)
ax1.set_xticks([-200, -150, -100, -50, 0, 50, 100, 150, 200])
ax1.set_xlim(-260, 260)
ax2.tick_params(axis='x', labelsize=14)
ax2.set_xticks([-1, 1])
ax1.set_xlabel('Total Score', fontsize = 20)
ax1.set_ylabel('Series', fontsize = 20)
ax2.set_xlabel('Position Difference', fontsize = 20)
ax1.set_yticks(ticks = y_values, labels = dq_change_plus['Series'].unique(), fontsize = 14)
plt.show()


# for series, name, pos_diff, in zip(dq_change['Series'], dq_change['Name'],
#                                 dq_change['Position Difference']):
#     plt.plot(series, pos_diff, '-o')
# plt.show()

# for series, name, pos_diff, in zip(dq_change['Series'], dq_change['Name'],
#                                 dq_change['Position Difference']):
#     plt.plot(series, pos_diff, 'o', label = name)
#     plt.legend()
# plt.show()

# for series, name, orig_pos, new_pos, pos_diff, in zip(dq_change['Series'], dq_change['Name'],
#                                 dq_change['Position'], dq_change['New Position'],
#                                 dq_change['Position Difference']):
#     plt.plot(series, orig_pos, 'o', label = name)
#     plt.plot(series, new_pos, 'x',label = name)
#     plt.legend()
# plt.show()

