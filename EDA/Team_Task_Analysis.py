import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import Team_Task_Functions as TTF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

team_table = TTF.formatting_team_table(dataframe = team_table)

TTF.plot_teams(dataframe = team_table)

#Split team tables based off group of 2 (A) or group of three (B)
team_two = team_table[team_table['Team'] == 'A'].reset_index(drop = True)
team_three = team_table[team_table['Team'] == 'B'].reset_index(drop = True)

team_combinations_all_series = TTF.team_combinations(series_grouped = False)
team_combinations_grouped = TTF.team_combinations(series_grouped = True)

team_task_totals, all_team_tasks = TTF.team_scores_per_seat(file_path = file_path, 
                                                            file_name = 'Taskmaster_Series_Scores_Cleaned.xlsx', 
                                                            combo_table = team_combinations_all_series)

team_task_totals = TTF.total_team_scores(team_table = team_task_totals)

team_task_totals = TTF.include_team_names(team_score_table = team_task_totals, 
                                           team_two_table = team_two, team_three_table = team_three)


# Determine percentage differences between Team A and Team B in each series
total_per_diff = TTF.percent_diff(score_team_A = team_task_totals['Team A Total'],
                              score_team_B = team_task_totals['Team B Total'])

total_person_diff = TTF.percent_diff(score_team_A = team_task_totals['Team_A_per_person'],
                              score_team_B = team_task_totals['Team_B_per_person'])

total_task_diff = TTF.percent_diff(score_team_A = team_task_totals['Team_A_per_task'],
                              score_team_B = team_task_totals['Team_B_per_task'])

total_person_task_diff = TTF.percent_diff(score_team_A = team_task_totals['Team_A_per_person_task'],
                              score_team_B = team_task_totals['Team_B_per_person_task'])

# Take the full team table and keep only wanted columns. e.g. remove Seat columns
all_teams = team_task_totals[['Series', 'Number', 'Team A Total', 'Team B Total',
       'Team_A_per_person', 'Team_B_per_person', 'Team_A_per_task',
       'Team_B_per_task', 'Team_A_per_person_task', 'Team_B_per_person_task',
       'Team A Names', 'Team B Names']]

#Get full Team A and Team B tables including all score method columns and names
team_A = team_task_totals[['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number',
       'Team_A', 'Series Number', 'Team A Total', 'Team_A_per_person', 'Team_A_per_task',
       'Team_A_per_person_task', 'Team A Names']]

team_B = team_task_totals[['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Number',
        'Team_B', 'Series Number', 'Team B Total', 'Team_B_per_person', 'Team_B_per_task',  
        'Team_B_per_person_task', 'Team B Names']]

# Sort Team A and Team B tables based on the total per person per task column.
team_A_top = team_A.sort_values(by = 'Team_A_per_person_task', ascending = False)
team_A_bottom = team_A.sort_values(by = 'Team_A_per_person_task', ascending = True)

team_B_top = team_B.sort_values(by = 'Team_B_per_person_task', ascending = False)
team_B_bottom = team_B.sort_values(by = 'Team_B_per_person_task', ascending = True)

team_name_scores = TTF.get_best_worse_teams(team_table = all_teams)


#########
#PLOTS
#########

#Percentage differnce bar charts for four team score methods
plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)

plt.bar(team_task_totals['Series Number']-0.3, total_per_diff, 
        width = 0.2, edgecolor = 'black', label = 'Total Team Score')
plt.bar(team_task_totals['Series Number']-0.1, total_person_diff, 
        width = 0.2, edgecolor = 'black', label = 'Team Score per Person')
plt.bar(team_task_totals['Series Number']+0.1, total_task_diff, 
        width = 0.2, edgecolor = 'black', label = 'Team Score per Task')
plt.bar(team_task_totals['Series Number']+0.3, total_person_task_diff, 
        width = 0.2, edgecolor = 'black', label = 'Score per Person per Task')
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Absolute Percentage Differences', fontsize = 20)
plt.title('Absolute Percentage Differences between Team of Three and Team \n of Two for Four Different Team Score Methods',
          fontsize = 18)
plt.legend(loc = 'upper right', fontsize = 16, ncol = 2)
plt.show()
    

# Next four plots show bar charts for the team scores from four different methods:
# 1. Sum Contestent scores for each team task to give total team score
# 2. Total team score per person (divide team total by number of team members)
# 3. Total team score per task (divide team total by number of tasks)
# 4. Total team score per person per tasks (divide team total by number of people and number of tasks

# Option 4 is the one to be carried out in further analysis because it averages the scores more fairly than
# options 2 or 3.

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

plt.bar(team_task_totals['Series Number']-0.2, team_task_totals['Team A Total'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Two')
plt.bar(team_task_totals['Series Number']+0.2, team_task_totals['Team B Total'], 
        width = 0.4, edgecolor = 'black', label = 'Team of Three')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team A Total'].idxmax(axis = 0)]-0.2, 
        team_task_totals['Team A Total'][team_task_totals['Team A Total'].idxmax(axis = 0)], color = 'darkblue',
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Two Score')
plt.bar(team_task_totals['Series Number'][team_task_totals['Team B Total'].idxmax(axis = 0)]+0.2, 
        team_task_totals['Team B Total'][team_task_totals['Team B Total'].idxmax(axis = 0)], color = 'darkred', 
        width = 0.4, edgecolor = 'black', label = 'Highest Team of Three Score')
plt.xlim(0.5, 20.5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Team Scores Total', fontsize = 20)
plt.title('Total Team Scores for Each Series', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16, ncol = 2)
plt.show()


plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)

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
plt.title('Total Team Scores per Number of Team Members for Each Series', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16, ncol = 2)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)

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
plt.title('Total Team Scores per Number of Tasks for Each Series', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16, ncol = 2)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)

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
plt.title('Total Team Scores per Number of Team Members and \n Number of Tasks for Each Series', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 16, ncol = 2)
plt.show()

#Top and Bottom 10 teams for all series

fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(10, 10), sharex = True)
plt.subplots_adjust(wspace=0, hspace=0.05, bottom=0.1, top=0.94, left=0.02, right=0.98)

df_top = team_name_scores.sort_values('TeamScoresPersonTask')[30:40]

df_top.plot.barh(y='TeamScoresPersonTask', x='Team Names', ax=ax1, color='red', alpha=0.8, 
                 edgecolor='white', width=0.9, label='Top Ten Teams')

for i, (score, team, series, tasks) in enumerate(zip(df_top['TeamScoresPersonTask'], df_top['Team Names'],
                                              df_top['Series'], df_top['Number'])):
    ax1.text(0.05, i, team, va='center', ha='left', fontsize=12, color='white')
    ax1.text(-0.85, i, series, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.5, i, tasks, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.2, i, score, va='center', ha='left', fontsize=12, color = 'red')
    ax1.text(-0.95, 10, 'Series  Number  Score', fontsize = 11, color = 'black')

ax1.set_xlim(-1, 6)
ax1.set_yticks([])
ax1.set_ylabel('')
ax1.legend(fontsize=16)

df_bottom = team_name_scores.sort_values('TeamScoresPersonTask')[0:10]

df_bottom.plot.barh(y='TeamScoresPersonTask', x='Team Names', ax=ax2, color='dodgerblue', alpha=0.8, 
                    edgecolor='white', width=0.9, label='Bottom 10 Teams')

for i, (score, team, series, tasks) in enumerate(zip(df_bottom['TeamScoresPersonTask'], df_bottom['Team Names'],
                                                     df_bottom['Series'], df_bottom['Number'])):
    ax2.text(0.05, i, team, va='center', ha='left',fontsize=12, color='black')
    ax2.text(-0.85, i, series, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.5, i, tasks, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.2, i, score, va='center', ha='left', fontsize=12, color = 'blue')

ax2.set_xlim(-1, 6)
ax2.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax2.set_yticks([]) 
ax2.legend(loc = 'best', fontsize=16)

fig.suptitle("Top and Bottom 10 Teams Across all Series", fontsize = 20)
plt.xlabel('Score Per Number of Tasks and Per Number of Team Members', fontsize=18)
plt.ylabel('')
ax1.tick_params(axis='x', labelsize=12)
ax2.tick_params(axis='x', labelsize=12)

plt.show()
