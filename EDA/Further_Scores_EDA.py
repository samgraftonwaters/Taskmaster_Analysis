import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
scores_series_table = file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx'

score_diff = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[2:7]

    final_scores = data[data['Task Number'] == f'Series {series} Grand Total'].reset_index(drop = True)

    final_scores = final_scores[contestents]

    diff_scores = final_scores.max(axis=1) - final_scores.min(axis = 1)

    score_diff.append([diff_scores.values[0], f'S{series}'])

score_diff = pd.DataFrame(score_diff, columns = ['Difference', 'Series'])
print(score_diff)

plt.bar(x = score_diff['Series'], height = score_diff['Difference'], color = 'blue', alpha = 0.7,
         edgecolor = 'black')


for i in range(0, 20):
    plt.text(i, score_diff['Difference'][i]+0.5, 
            score_diff['Difference'][i], ha='center', fontsize = 14, color = 'blue')

plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlim(-0.6, 19.6)
plt.xlabel('Series', fontsize = 18)
plt.ylabel('Difference in Scores', fontsize = 18)
plt.title('Difference in Scores between Winner and Loser per Series', fontsize = 20)
plt.show()

