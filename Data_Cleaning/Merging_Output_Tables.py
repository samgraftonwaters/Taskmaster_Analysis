import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

DQ_table = pd.read_csv(file_path + 'DQ_Table.csv')
Episode_win_loss = pd.read_csv(file_path + 'Episode Wins and Losses.csv')
gender_age = pd.read_csv(file_path + 'Gender_Age_Series_Scores.csv')
count_fives = pd.read_csv(file_path + 'Number of Fives Scored.csv') 
count_ones = pd.read_csv(file_path + 'Number of Ones Scored.csv')
# most_eps_lost = pd.read_csv(file_path + 'Most Episodes Lost.csv') 
# most_eps_wins = pd.read_csv(file_path + 'Most Episodes Won.csv') 
team_A = pd.read_csv(file_path + 'Team A Results.csv') 
team_B = pd.read_csv(file_path + 'Team B Results.csv') 
team_scores = pd.read_csv(file_path + 'Team_Scores.csv') 
tie_losers = pd.read_csv(file_path + 'Tie_Break_Losers.csv') 
tie_winners = pd.read_csv(file_path + 'Tie_Break_Winners.csv') 
final_score_positions = pd.read_csv(file_path + 'Total Final Scores and Positions.csv')
avg_episode_scores = pd.read_csv(file_path + 'Avg Episode Scores and Positions.csv')
avg_task_scores = pd.read_csv(file_path + 'Avg Task Scores and Positions.csv')

tables = {"DQ_table": DQ_table, "Episode_win_loss": Episode_win_loss, "gender_age": gender_age, 
          "count_fives": count_fives, "most_fives": count_ones, "team_A": team_A, "team_B": team_B, "team_scores": team_scores,
          "tie_losers": tie_losers, "tie_winners": tie_winners, "final_score_positions": final_score_positions, 
          'avg_episode_scores' : avg_episode_scores, 'avg_task_scores' : avg_task_scores,
          #"most_eps_lost": most_eps_lost,  "most_eps_wins": most_eps_wins,
          }

for name, df in tables.items():
    print(f"{name}")
    print(df.columns.tolist())
    print()

#Overall and Average Scores
avg_episode_scores = avg_episode_scores.rename(columns = {'Score' : 'Avg Score per Episodes'}).drop(['Series', 'Seat', 'Position'], axis = 1)
avg_task_scores = avg_task_scores.rename(columns = {'Score' : 'Avg Score per Tasks'}).drop(['Series', 'Seat', 'Position'], axis = 1)

merged_scores_table = pd.merge(left = final_score_positions, right = avg_episode_scores, on = 'Name', how = 'left')
merged_scores_table = pd.merge(left = merged_scores_table, right = avg_task_scores, on = 'Name', how = 'left')

print(merged_scores_table.head())

#counts ones/fives merged tables
count_fives_ones = pd.merge(left = count_fives.drop(['Series', 'Seat'], axis = 1), 
                 right = count_ones.drop(['Series', 'Seat'], axis = 1), on = 'Name', how = 'left')

print(count_fives_ones.head())

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
print(tie_breaks.head())

#Removing columns from DQ, Gender/Age and Episode columns

DQ_table = DQ_table.drop(['Series', 'Seat'], axis = 1)
gender_age = gender_age.drop(['Series', 'Score', 'Seat', 'Position', 'Birth_Date', 'Age_at_First_Air', 'Series Number'], axis = 1)
gender_age = gender_age.rename(columns = {'Age_at_First_Air' : 'Age'})
Episode_win_loss = Episode_win_loss.drop(['Series', 'Seat'], axis = 1)
Episode_win_loss = Episode_win_loss.rename(columns = {'Wins' : 'Episode Wins', 'Losses' : 'Episode Losses', 
                                                      'Percentage_Won' : 'Episode Percentage Wins', 
                                                      'Percentage_Lost' : 'Episode Percentage Lossses'})

print(DQ_table.head())
print(gender_age.head())
print(Episode_win_loss.head())