import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import Team_Task_Functions as TTF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

team_table = TTF.formatting_team_table(dataframe = team_table)

TTF.plot_teams(dataframe = team_table)

team_two = team_table[team_table['Team'] == 'A'].reset_index(drop = True)
team_three = team_table[team_table['Team'] == 'B'].reset_index(drop = True)

combo_table = {
    "Team_A" : [[1, 5], [3, 5], [4, 5], [1, 4], [3, 4], [2, 3], [2, 5], [1, 3], [2, 4], [1, 2]],
    "Team_B" : [[2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 5], [1, 2, 5], [1, 4, 5], [1, 3, 4], [2, 4, 5], 
                [1, 3, 5], [3, 4, 5]],
    "Series" : [[1, 10, 12], [2, 17], [3, 14, 16, 18], [4, 6], [5, 11], [7], [8, 19], [9, 13], [20], [15]],
    "Combos" : [3, 2, 4, 2, 2, 1, 2, 2, 1, 1]
}

team_combos = pd.DataFrame(combo_table)
print(team_combos.head(10))

combo_table = {
    "Team_A" : [[1, 5], [1, 5], [1, 5], [3, 5], [3, 5], [4, 5], [4, 5], [4, 5], [4, 5], [1, 4], [1, 4],
                [3, 4], [3, 4], [2, 3], [2, 5], [2, 5], [1, 3], [1, 3], [2, 4], [1, 2]],
    "Team_B" : [[2, 3, 4], [2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3], 
                [1, 2, 3], [2, 3, 5], [2, 3, 5], [1, 2, 5], [1, 2, 5], [1, 4, 5], [1, 3, 4], [1, 3, 4], 
                [2, 4, 5], [2, 4, 5], [1, 3, 5], [3, 4, 5]],
    "Series Number" : [1, 10, 12, 2, 17, 3, 14, 16, 18, 4, 6, 5, 11, 7, 8, 19, 9, 13, 20, 15],
}

team_combinations = pd.DataFrame(combo_table).sort_values(by = 'Series Number').reset_index(drop = True)
print(team_combinations.head(20))

all_team_tasks = []
team_task_totals = []
team_tasks_series = []

for series in range(1, 21):

    data = pd.read_excel(file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx', sheet_name = f'Series_{series}')

    
    data.rename(columns = {data.columns[2] : 'Seat 1', data.columns[3] : 'Seat 2', 
                                  data.columns[4] : 'Seat 3', data.columns[5] : 'Seat 4', 
                                  data.columns[6] : 'Seat 5'}, inplace = True)
    cols = data.columns
    seats = cols[2:7]

    team_tasks = data[data['Team Task'] == 1].reset_index(drop = True)

    team_tasks = team_tasks.drop(['Prize Task', 'Live Task', 'Tie Break', 'Solo Task'], axis = 1)
    
    all_team_tasks.append(team_tasks)
    
    ###

    team_tasks_summed = team_tasks[seats].sum(axis = 0).astype(int)

    team_tasks_summed['Series'] = f'S{series}'

    team_task_totals.append(team_tasks_summed)

    ###
    
    num_team_tasks = len(team_tasks[team_tasks['Extra Part'] != 1])

    team_tasks_series.append(num_team_tasks)

all_team_tasks = pd.DataFrame(np.vstack(all_team_tasks), columns = ['Task Number', 'Description', 'Seat 1', 'Seat 2', 'Seat 3', 'Seat 4',
       'Seat 5', 'Tasknumber', 'Episode', 'Series', 'Team Task', 'Extra Part'])
team_task_totals = pd.DataFrame(np.vstack(team_task_totals), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series'])
team_tasks_series = pd.DataFrame(np.vstack(team_tasks_series), columns = ['Number'])

team_task_totals = pd.concat([team_task_totals, team_tasks_series, team_combinations], axis = 1)

print(all_team_tasks)
print(team_task_totals)


A_total = []
B_total = []
for series in range(0, 20):

    a1 = team_task_totals['Team_A'][series][0]
    a2 = team_task_totals['Team_A'][series][1]

    b1 = team_task_totals['Team_B'][series][0]
    b2 = team_task_totals['Team_B'][series][1]
    b3 = team_task_totals['Team_B'][series][2]

    a_total = team_task_totals[f'Seat {a1}'][series] + team_task_totals[f'Seat {a2}'][series]
    b_total = team_task_totals[f'Seat {b1}'][series] + team_task_totals[f'Seat {b2}'][series] + team_task_totals[f'Seat {b3}'][series]

    A_total.append(a_total)
    B_total.append(b_total)

team_task_totals = pd.concat([team_task_totals, pd.DataFrame(A_total, columns = ['Team A Total']), 
                              pd.DataFrame(B_total, columns = ['Team B Total'])], axis = 1)

team_task_totals['Team_A_per_person'] = round(team_task_totals['Team A Total'] / 2, 1)
team_task_totals['Team_B_per_person'] = round(team_task_totals['Team B Total'] / 3, 1)

print(team_task_totals.head())

team_task_totals['Team_A_per_task'] = round(team_task_totals['Team A Total'] / team_task_totals['Number'], 1)
team_task_totals['Team_B_per_task'] = round(team_task_totals['Team B Total'] / team_task_totals['Number'], 1)

team_task_totals['Team_A_per_person_task'] = round(team_task_totals['Team_A_per_person'] / team_task_totals['Number'], 1)
team_task_totals['Team_B_per_person_task'] = round(team_task_totals['Team_B_per_person'] / team_task_totals['Number'], 1)

print(team_task_totals.head(10))

team_A_names = []
team_B_names = []

for series in range(1, 21):

    names_A = team_two[team_two['Series Number'] == series]['Name'].to_list()

    names_B = team_three[team_three['Series Number'] == series]['Name'].to_list()

    team_A_names.append([names_A])

    team_B_names.append([names_B])

team_task_totals = pd.concat([team_task_totals, pd.DataFrame(team_A_names, columns = ['Team A Names']), 
                              pd.DataFrame(team_B_names, columns = ['Team B Names'])], axis = 1)


print(team_task_totals.columns)



plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

plt.bar(team_task_totals['Series Number']-0.2, team_task_totals['Team_A_per_person'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Two')
plt.bar(team_task_totals['Series Number']+0.2, team_task_totals['Team_B_per_person'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Three')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_A_per_person'].idxmax(axis = 0)]-0.2, team_task_totals['Team_A_per_person'][team_task_totals['Team_A_per_person'].idxmax(axis = 0)], color = 'darkblue',
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Two Score')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_B_per_person'].idxmax(axis = 0)]+0.2, team_task_totals['Team_B_per_person'][team_task_totals['Team_B_per_person'].idxmax(axis = 0)], color = 'darkred', 
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Three Score')
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Team Scores per Number of People', fontsize = 20)
plt.legend(loc = 'upper left', fontsize = 16)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

plt.bar(team_task_totals['Series Number']-0.2, team_task_totals['Team_A_per_task'],
        width = 0.4, edgecolor = 'black', label = 'Team of Two')
plt.bar(team_task_totals['Series Number']+0.2, team_task_totals['Team_B_per_task'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Three')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_A_per_task'].idxmax(axis = 0)]-0.2, team_task_totals['Team_A_per_task'][team_task_totals['Team_A_per_task'].idxmax(axis = 0)], color = 'darkblue',
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Two Score')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_B_per_task'].idxmax(axis = 0)]+0.2, team_task_totals['Team_B_per_task'][team_task_totals['Team_B_per_task'].idxmax(axis = 0)], color = 'darkred', 
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Three Score')
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Team Scores per Number of Tasks', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

plt.bar(team_task_totals['Series Number']-0.2, team_task_totals['Team_A_per_person_task'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Two')
plt.bar(team_task_totals['Series Number']+0.2, team_task_totals['Team_B_per_person_task'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Three')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_A_per_person_task'].idxmax(axis = 0)]-0.2, team_task_totals['Team_A_per_person_task'][team_task_totals['Team_A_per_person_task'].idxmax(axis = 0)], color = 'darkblue',
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Two Score')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team_B_per_person_task'].idxmax(axis = 0)]+0.2, team_task_totals['Team_B_per_person_task'][team_task_totals['Team_B_per_person_task'].idxmax(axis = 0)], color = 'darkred', 
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Three Score')
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Team Scores per Number of People and Tasks', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16)
plt.show()

team_A = team_task_totals[['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number',
       'Team_A', 'Series Number', 'Team A Total', 'Team_A_per_person', 'Team_A_per_task',
       'Team_A_per_person_task', 'Team A Names']]

team_B = team_task_totals[['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number',
        'Team_B', 'Series Number', 'Team B Total', 'Team_B_per_person', 'Team_B_per_task',  
        'Team_B_per_person_task', 'Team B Names']]

team_A_top = team_A.sort_values(by = 'Team_A_per_person_task', ascending = False)
team_A_bottom = team_A.sort_values(by = 'Team_A_per_person_task', ascending = True)

team_B_top = team_B.sort_values(by = 'Team_B_per_person_task', ascending = False)
team_B_bottom = team_B.sort_values(by = 'Team_B_per_person_task', ascending = True)

all_teams = team_task_totals[['Series', 'Number', 'Team A Total', 'Team B Total',
       'Team_A_per_person', 'Team_B_per_person', 'Team_A_per_task',
       'Team_B_per_task', 'Team_A_per_person_task', 'Team_B_per_person_task',
       'Team A Names', 'Team B Names']]

plt.plot(all_teams['Number'], all_teams['Team_A_per_person_task'], 'o')
plt.plot(all_teams['Number'], all_teams['Team_B_per_person_task'], 'o')
plt.show()

plt.plot(all_teams['Team_A_per_person_task'], all_teams['Team_B_per_person_task'], 'o')
plt.grid()
plt.show()

print(all_teams['Team_A_per_person_task'].unique(), len(all_teams['Team_A_per_person_task'].unique()))
print(all_teams['Team_B_per_person_task'].unique(), len(all_teams['Team_B_per_person_task'].unique()))

team_name_table = all_teams.melt(id_vars='Series', value_vars=['Team A Names', 'Team B Names'], value_name='Team Names')#.drop('variable', axis=1)
team_name_table = team_name_table.rename({'variable' : 'Team'}, axis = 1)
team_name_table['Team'] = team_name_table['Team'].str.replace('Team ', '').str.replace(' Names', '')
team_person_task = all_teams.melt(id_vars='Series', value_vars=['Team_A_per_person_task', 'Team_B_per_person_task'], value_name='TeamScoresPersonTask').drop('variable', axis=1)

team_name_scores = pd.concat([team_name_table, team_person_task.drop('Series', axis = 1)], axis = 1)

number_tasks = all_teams[['Series', 'Number']]

team_name_scores = pd.merge(team_name_scores, number_tasks, how = 'left', on = 'Series')

team_name_scores['Team Names'] = team_name_scores['Team Names'].apply(lambda x: ', '.join(map(str, x)))

team_name_scores_top = team_name_scores.sort_values(by = 'TeamScoresPersonTask', ascending = False).reset_index(drop = True)

team_name_scores_bottom = team_name_scores.sort_values(by = 'TeamScoresPersonTask', ascending = True).reset_index(drop = True)

team_name_scores = team_name_scores.sort_values(by = 'TeamScoresPersonTask', ascending = False).reset_index(drop = True)

plt.plot(team_name_scores['Number'], team_name_scores['TeamScoresPersonTask'], 'o')
plt.grid()
plt.show()

print(team_name_scores_top[0:10])
print(team_name_scores_top.info())
print(team_name_scores_bottom[0:10])
print(len(team_name_scores_bottom))




# y = np.arange(0, 10, 1)

# fig, (ax1, ax2) = plt.subplots(ncols = 1, nrows = 2)
# plt.subplots_adjust(wspace=0, hspace=0.05, bottom = 0.1, top = 0.94, left = 0.33, right = 0.99)

# team_name_scores.sort_values('TeamScoresPersonTask')[30:40].plot.barh(y = 'TeamScoresPersonTask', 
#                                                                       x = 'Team Names', ax = ax1,
#                                                                       width = 0.9, 
#                                                                       color = 'red', alpha = 0.8,
#                                                                       edgecolor = 'black', label = 'Top Ten Teams')
# ax1.set_xlim(0, 6)
# ax1.set_xticks([],[])
# ax1.legend(fontsize = 16)
# team_name_scores.sort_values('TeamScoresPersonTask')[0:10].plot.barh(y = 'TeamScoresPersonTask',
#                                                                      x = 'Team Names', ax = ax2,
#                                                                      width = 0.9, 
#                                                                      color = 'blue', alpha = 0.8,
#                                                                      edgecolor = 'black', label = 'Bottom 10 Teams')
# ax2.set_xlim(0, 6)
# ax2.legend(fontsize = 16)
# plt.xlabel('Score Per Number of Tasks and Per Number of Team Members', fontsize = 18)
# plt.ylabel('Teams', fontsize = 18)
# ax1.tick_params(axis='both', labelsize=12)
# ax2.tick_params(axis='both', labelsize=12)

# plt.show()

# print(team_A_top.head())
# print(team_A_bottom.head())
# print(team_B_top.head())
# print(team_B_bottom.head())

fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(10, 10), sharex = True)
plt.subplots_adjust(wspace=0, hspace=0.05,
                    bottom=0.1, top=0.94,
                    left=0.1, right=0.99)

# ----- TOP 30–40 -----
df_top = team_name_scores.sort_values('TeamScoresPersonTask')[30:40]

df_top.plot.barh(y='TeamScoresPersonTask', x='Team Names', ax=ax1, color='red', alpha=0.8, 
                 edgecolor='black', width=0.9, label='Top Ten Teams')

ax1.set_xlim(-1, 6)
ax1.set_yticks([])
ax1.set_ylabel('Team', fontsize = 16)  # remove y-axis labels
ax1.legend(fontsize=16)

# Add team names inside bars
for i, (score, team, series, tasks) in enumerate(zip(df_top['TeamScoresPersonTask'], df_top['Team Names'],
                                              df_top['Series'], df_top['Number'])):
    ax1.text(0.05, i, team, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.75, i, series, va='center', ha='left', fontsize=12, color='black')
    ax1.text(3, i, tasks, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.3, i, score, va='center', ha='left', fontsize=12, color = 'red')
# ----- BOTTOM 0–10 -----
df_bottom = team_name_scores.sort_values('TeamScoresPersonTask')[0:10]

df_bottom.plot.barh(y='TeamScoresPersonTask', x='Team Names', ax=ax2, color='lightblue', alpha=0.8, 
                    edgecolor='black', width=0.9, label='Bottom 10 Teams')

ax2.set_xlim(-1, 6)
ax2.set_yticks([])  # remove y-axis labels
ax2.legend(loc = 'best', fontsize=16)

# Add team names inside bars
for i, (score, team, series, tasks) in enumerate(zip(df_bottom['TeamScoresPersonTask'], df_bottom['Team Names'],
                                                     df_top['Series'], df_top['Number'])):
    ax2.text(0.05, i, team, va='center', ha='left',fontsize=12, color='black')
    ax2.text(-0.75, i, series, va='center', ha='left', fontsize=12, color='black')
    ax2.text(3, i, tasks, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.3, i, score, va='center', ha='left', fontsize=12, color = 'blue')

# Shared labels
plt.xlabel('Score Per Number of Tasks and Per Number of Team Members', fontsize=18)
plt.ylabel('Teams', fontsize=18)

ax1.tick_params(axis='x', labelsize=12)
ax2.tick_params(axis='x', labelsize=12)

plt.show()
