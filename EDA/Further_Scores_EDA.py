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

plt.bar(x = score_diff['Series'], height = score_diff['Difference'], width = 0.8,
        color = 'blue', alpha = 0.7, edgecolor = 'black')

plt.bar(score_diff['Series'][score_diff['Difference'].idxmax(axis = 0)], 
        score_diff['Difference'][score_diff['Difference'].idxmax(axis = 0)], color = 'darkorange',
        edgecolor = 'black', label = 'Biggest Difference')

plt.bar(score_diff['Series'][score_diff['Difference'].idxmin(axis = 0)], 
        score_diff['Difference'][score_diff['Difference'].idxmin(axis = 0)], color = 'yellow',
        edgecolor = 'black', label = 'Smallest Difference')

for i in range(0, 20):
    plt.text(i, score_diff['Difference'][i]+0.5, 
            score_diff['Difference'][i], ha='center', fontsize = 14, color = 'blue')

plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlim(-0.6, 19.6)
plt.xlabel('Series', fontsize = 18)
plt.ylabel('Difference in Scores', fontsize = 18)
plt.title('Difference in Scores between Winner and Loser per Series', fontsize = 20)
plt.legend(fontsize = 16)
plt.show()



count_five = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[2:7]

    scores = data[data['Task Number'] != f'Series {series} Grand Total'].reset_index(drop = True)

    scores = scores[contestents]

    count_scores = scores[scores == 5].count(axis = 0)

    count_five.append(count_scores)

print(count_five)
count_five = pd.DataFrame(np.vstack(count_five), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'])
series = []
for i in range(20):
    series.append(f'S{count_five.index.values[i] + 1}')
count_five['Series'] = series
print(count_five)

for seat in range(1, 6):
    most_fives = count_five[['Series', f'Seat {seat}']]
    most_fives = most_fives[f'Seat {seat}'].max(axis = 0)
    print(most_fives)