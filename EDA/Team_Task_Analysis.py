import pandas as pd
import numpy as np
import Team_Task_Functions as TTF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

team_table = TTF.formatting_team_table(dataframe = team_table)

print(team_table.head())

team_two = team_table[team_table['Team'] == 'A']
team_three = team_table[team_table['Team'] == 'B']

