import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import Team_Task_Functions as TTF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

team_table = TTF.formatting_team_table(dataframe = team_table)

TTF.plot_teams(dataframe = team_table)

team_two = team_table[team_table['Team'] == 'A']
team_three = team_table[team_table['Team'] == 'B']

combo_table = {"Team_A" : [[1, 5], [3, 5], [4, 5], [1, 4], [3, 4], [2, 3], [2, 5], [1, 3], [2, 4], [1, 2]],
"Team_B" : [[2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 5], [1, 2, 5], [1, 4, 5], [1, 3, 4], [2, 4, 5], [1, 3, 5], [3, 4, 5]],
"Series" : [[1, 10, 12], [2, 17], [3, 14, 16, 18], [4, 6], [5, 11], [7], [8, 19], [9, 13], [20], [15]],
"Combos" : [3, 2, 4, 2, 2, 1, 2, 2, 1, 1]
}

team_combinatins = pd.DataFrame(combo_table)
print(team_combinatins.head(10))


combo_table = {"Team_A" : [[1, 5], [1, 5], [1, 5], [3, 5], [3, 5],
                          [4, 5], [4, 5], [4, 5], [4, 5], [1, 4], [1, 4],
                          [3, 4], [3, 4], [2, 3], [2, 5], [2, 5],
                          [1, 3], [1, 3], [2, 4], [1, 2]],
"Team_B" : [[2, 3, 4],  [2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 4], 
            [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], 
            [2, 3, 5], [2, 3, 5], [1, 2, 5], [1, 2, 5],
            [1, 4, 5], [1, 3, 4], [1, 3, 4],
            [2, 4, 5], [2, 4, 5], [1, 3, 5], [3, 4, 5]],
"Series" : [1, 10, 12, 2, 17, 3, 14, 16, 18, 4, 6, 5, 11, 7, 8, 19, 9, 13, 20, 15],
}

team_combinatins = pd.DataFrame(combo_table).sort_values(by = 'Series').reset_index(drop = True)
print(team_combinatins.head(20))





