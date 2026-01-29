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
least_fives = pd.read_csv(file_path + 'Least_Fives_Table.csv') 
most_fives = pd.read_csv(file_path + 'Most_Fives_Table.csv')
least_ones = pd.read_csv(file_path + 'Least_Ones_Table.csv') 
most_ones = pd.read_csv(file_path + 'Most_Ones_Table.csv') 
most_eps_lost = pd.read_csv(file_path + 'Most Episodes Lost.csv') 
most_eps_wins = pd.read_csv(file_path + 'Most Episodes Won.csv') 
team_A = pd.read_csv(file_path + 'Team A Results.csv') 
team_B = pd.read_csv(file_path + 'Team B Results.csv') 
team_scores = pd.read_csv(file_path + 'Team_Scores.csv') 
tie_losers = pd.read_csv(file_path + 'Tie_Break_Losers.csv') 
tie_winners = pd.read_csv(file_path + 'Tie_Break_Winners.csv') 
final_score_positions = pd.read_csv(file_path + 'Total Final Scores and Positions.csv')
avg_episode_scores = pd.read_csv(file_path + 'Avg Episode Scores and Positions.csv')
avg_task_scores = pd.read_csv(file_path + 'Avg Task Scores and Positions.csv')

tables = {"DQ_table": DQ_table, "Episode_win_loss": Episode_win_loss, "gender_age": gender_age, 
          "least_fives": least_fives, "most_fives": most_fives, "least_ones": least_ones, 
          "most_ones": most_ones, "most_eps_lost": most_eps_lost, "most_eps_wins": most_eps_wins, 
          "team_A": team_A, "team_B": team_B, "team_scores": team_scores, "tie_losers": tie_losers, 
          "tie_winners": tie_winners, "final_score_positions": final_score_positions, 
          'avg_episode_scores' : avg_episode_scores, 'avg_episode_scores' : avg_task_scores}

for name, df in tables.items():
    print(f"{name}")
    print(df.columns.tolist())
    print()

