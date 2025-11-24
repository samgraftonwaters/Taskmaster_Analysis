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
plt.bar(team_task_totals['Series Number'][13]-0.2, team_task_totals['Team_A_per_person'][13], color = 'darkblue',
        width = 0.4, edgecolor = 'black', label = 'Team of Two')
plt.bar(team_task_totals['Series Number'][16]+0.2, team_task_totals['Team_B_per_person'][16], color = 'darkred', 
        width = 0.4, edgecolor = 'black', label = 'Team of Three')
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
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Team Scores per Number of People and Tasks', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16)
plt.show()


