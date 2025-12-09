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

plt.bar(x = score_diff['Series'], height = score_diff['Difference'])
plt.show()

