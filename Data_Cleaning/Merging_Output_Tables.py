import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

DQ_table = pd.read_csv(file_path + 'DQ_Table.csv', encoding="utf-8")
Episode_win_loss = pd.read_csv(file_path + 'Episode Wins and Losses.csv', encoding="utf-8")
gender_age = pd.read_csv(file_path + 'Gender_Age_Series_Scores.csv', encoding="utf-8")
count_fives = pd.read_csv(file_path + 'Number of Fives Scored.csv', encoding="utf-8") 
count_ones = pd.read_csv(file_path + 'Number of Ones Scored.csv', encoding="utf-8")
percent_fives = pd.read_csv(file_path + 'Percent of Fives Scored.csv')
percent_ones = pd.read_csv(file_path + 'Percent of Ones Scored.csv')
number_tasks = pd.read_csv(file_path + 'Total Scores per Number of Tasks.csv')
team_A = pd.read_csv(file_path + 'Team A Results.csv', encoding="utf-8") 
team_B = pd.read_csv(file_path + 'Team B Results.csv', encoding="utf-8") 
tie_losers = pd.read_csv(file_path + 'Tie_Break_Losers.csv', encoding="utf-8") 
tie_winners = pd.read_csv(file_path + 'Tie_Break_Winners.csv', encoding="utf-8") 
final_score_positions = pd.read_csv(file_path + 'Total Final Scores and Positions.csv', encoding="utf-8")
avg_episode_scores = pd.read_csv(file_path + 'Avg Episode Scores and Positions.csv', encoding="utf-8")
avg_task_scores = pd.read_csv(file_path + 'Avg Task Scores and Positions.csv', encoding="utf-8")


print(Episode_win_loss[Episode_win_loss['Name'] == 'Mae Martin'])

tables = {"DQ_table": DQ_table, "Episode_win_loss": Episode_win_loss, "gender_age": gender_age, 
          "count_fives": count_fives, "most_fives": count_ones, "percent_fives" : percent_fives,
          "percent_ones" : percent_ones, "number_tasks" : number_tasks, "team_A": team_A, 
          "team_B": team_B, "tie_losers": tie_losers, "tie_winners": tie_winners, 
          "final_score_positions": final_score_positions, 'avg_episode_scores' : avg_episode_scores, 
          'avg_task_scores' : avg_task_scores}

for name, df in tables.items():
    print(f"{name}")
    print(df.columns.tolist())
    print()

#Overall and Average Scores
avg_episode_scores = avg_episode_scores.rename(columns = {'Score' : 'Avg Score per Episodes'}).drop(['Series', 'Seat', 'Position'], axis = 1)
avg_task_scores = avg_task_scores.rename(columns = {'Score' : 'Avg Score per Tasks'}).drop(['Series', 'Seat', 'Position'], axis = 1)

merged_scores_table = pd.merge(left = final_score_positions, right = avg_episode_scores, on = 'Name', how = 'left')
merged_scores_table = pd.merge(left = merged_scores_table, right = avg_task_scores, on = 'Name', how = 'left')

#counts ones/fives merged tables
count_fives_ones = pd.merge(left = count_fives.drop(['Series', 'Seat'], axis = 1), 
                 right = count_ones.drop(['Series', 'Seat'], axis = 1), on = 'Name', how = 'left')


percent_fives = pd.merge(left = percent_fives, 
                             right = number_tasks.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 
                                                        'Seat 5'], axis = 1), 
                            on = 'Series', how = 'left')

percent_fives_ones = pd.merge(left = percent_fives.drop(['Series', 'Seat'], axis = 1), 
                 right = percent_ones.drop(['Series', 'Seat'], axis = 1), on = 'Name', how = 'left')

print(percent_fives_ones)


#Tie Breaks
tie_winners = (tie_winners.drop(['Series', 'Seat', 'Double Losers'], axis = 1)
               .rename(columns = {'Tie breaks per series' : 'Tie breaks per series wins', 
                                  'Tie Breaks per Person' : 'Tie Breaks per Person wins'}))

tie_losers = (tie_losers.drop(['Series', 'Seat', 'Double Losers'], axis = 1)
              .rename(columns = {'Tie breaks per series' : 'Tie breaks per series losses',
                                 'Tie Breaks per Person' : 'Tie Breaks per Person losses'}))
                 
tie_breaks = pd.merge(left = tie_winners, right = tie_losers, how = 'outer', on = 'Name')

tie_breaks['Losses'] = tie_breaks['Losses'].fillna(0).astype(int)
tie_breaks['Wins'] = tie_breaks['Wins'].fillna(0).astype(int)
tie_breaks['Tie Breaks per Person'] = tie_breaks[['Tie Breaks per Person wins', 'Tie Breaks per Person losses']].bfill(axis=1).iloc[:, 0].astype(int)
tie_breaks['Tie Breaks per series'] = tie_breaks[['Tie breaks per series wins', 'Tie breaks per series losses']].bfill(axis=1).iloc[:, 0].astype(int)
tie_breaks = tie_breaks.drop(['Tie Breaks per Person wins', 'Tie Breaks per Person losses', 
                              'Tie breaks per series wins', 'Tie breaks per series losses'], axis = 1)
tie_breaks = tie_breaks.rename(columns = {'Wins' : 'Tie Break Wins', 'Losses' : 'Tie Break Losses'})

#Removing columns from DQ, Gender/Age and Episode columns

DQ_table = DQ_table.drop(['Series', 'Seat'], axis = 1)
gender_age = gender_age.drop(['Series', 'Score', 'Seat', 'Position', 'Birth_Date', 'Age_at_First_Air'], axis = 1)
gender_age = gender_age.rename(columns = {'Age_at_First_Air' : 'Age'})
Episode_win_loss = Episode_win_loss.drop(['Series', 'Seat'], axis = 1)
Episode_win_loss = Episode_win_loss.rename(columns = {'Wins' : 'Episode Wins', 'Losses' : 'Episode Losses', 
                                                      'Percentage_Won' : 'Episode Percentage Wins', 
                                                      'Percentage_Lost' : 'Episode Percentage Losses'})

#Teams tables

team_A = team_A.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Series Number', 'Team A Names', 'Team_A'], axis = 1)
team_A = team_A.melt(id_vars=[c for c in team_A.columns if c not in ["Name A1", "Name A2"]],
    value_vars=["Name A1", "Name A2"], var_name="Name_Position", value_name="Name").drop("Name_Position", axis = 1)
team_A = team_A.rename(columns = {'Number' : 'Number Team Tasks', 'Team A Total' : 'Team Total', 
                                  'Team_A_per_person' : 'Team Score per Person', 'Team_A_per_task' : 'Team Score per Task',
                                  'Team_A_per_person_task' : 'Team Score per Person Task'})
team_A['Team'] = 'A'

team_B = team_B.drop(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series', 'Series Number', 'Team B Names', 'Team_B'], axis = 1)
team_B = team_B.melt(id_vars=[c for c in team_B.columns if c not in ["Name B1", "Name B2", 'Name B3']],
    value_vars=["Name B1", "Name B2", 'Name B3'], var_name="Name_Position", value_name="Name").drop("Name_Position", axis = 1)
team_B = team_B.rename(columns = {'Number' : 'Number Team Tasks', 'Team B Total' : 'Team Total', 
                                  'Team_B_per_person' : 'Team Score per Person', 'Team_B_per_task' : 'Team Score per Task',
                                  'Team_B_per_person_task' : 'Team Score per Person Task'})
team_B['Team'] = 'B'
team_tasks = pd.concat([team_A, team_B], axis = 0)


print(merged_scores_table.head())
print(count_fives_ones.head())
print(percent_fives_ones.head())
print(tie_breaks.head())
print(DQ_table.head())
print(gender_age.head())
print(Episode_win_loss.head())
print(team_tasks.head())

dq_tie = pd.merge(left = tie_breaks, right = DQ_table, on = 'Name', how = 'left')
score_points = pd.merge(left = merged_scores_table, right = count_fives_ones, on = 'Name', how = 'left')
score_points = pd.merge(left = score_points, right = percent_fives_ones, on = 'Name', how = 'left')
gender_age_eps = pd.merge(left = gender_age, right = Episode_win_loss, on = 'Name', how = 'left')

merged_contestent_table = pd.merge(left = score_points, right = dq_tie, on = 'Name', how = 'left')
merged_contestent_table = pd.merge(left = merged_contestent_table, right = gender_age_eps, on = 'Name', how = 'left')
merged_contestent_table = pd.merge(left = merged_contestent_table, right = team_tasks, on = 'Name', how = 'left')

merged_contestent_table = merged_contestent_table.sort_values(by = ['Series Number', 'Seat'], ascending = True).reset_index(drop = True)
merged_contestent_table = merged_contestent_table.fillna(0)
print(merged_contestent_table.isna().sum())

print(merged_contestent_table)
print(len(merged_contestent_table))

merged_contestent_table.to_csv(output_path + 'Full Contestent Table.csv', sep = ',', index = False, encoding="utf-8")
