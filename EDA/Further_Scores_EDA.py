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


#Number of times contestents got 1 or 5 points.
#Then finds the most and least for each points category for each seat
count_five = []
count_one = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[2:7]

    scores = data[data['Task Number'] != f'Series {series} Grand Total'].reset_index(drop = True)

    scores = scores[contestents]

    count_scores_one = scores[scores == 1].count(axis = 0)
    count_scores_five = scores[scores == 5].count(axis = 0)

    count_one.append(count_scores_one)
    count_five.append(count_scores_five)

count_one = pd.DataFrame(np.vstack(count_one), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'])
count_five = pd.DataFrame(np.vstack(count_five), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'])

print(count_one)
print(count_five)

series = []
for i in range(20):
    series.append(f'S{count_five.index.values[i] + 1}')
count_one['Series'] = series
count_five['Series'] = series

most_ones = []
least_ones = []

most_fives = []
least_fives = []
for seat in range(1, 6):
    ones = count_one[['Series', f'Seat {seat}']]
    fives = count_five[['Series', f'Seat {seat}']]

    mostones = ones[ones[f'Seat {seat}'] == ones[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
    mostones['Seat'] = f'Seat {seat}'
    most_ones.append(mostones)
    
    leastones = ones[ones[f'Seat {seat}'] == ones[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
    leastones['Seat'] = f'Seat {seat}'
    least_ones.append(leastones)

    mostfives = fives[fives[f'Seat {seat}'] == fives[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
    mostfives['Seat'] = f'Seat {seat}'
    most_fives.append(mostfives)
    
    leastfives = fives[fives[f'Seat {seat}'] == fives[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
    leastfives['Seat'] = f'Seat {seat}'
    least_fives.append(leastfives)

most_ones = pd.DataFrame(np.vstack(most_ones), columns = ['Series', 'Number 1s', 'Seat'])
least_ones = pd.DataFrame(np.vstack(least_ones), columns = ['Series', 'Number 1s', 'Seat'])
print(most_ones)
print(least_ones)

most_fives = pd.DataFrame(np.vstack(most_fives), columns = ['Series', 'Number 5s', 'Seat'])
least_fives = pd.DataFrame(np.vstack(least_fives), columns = ['Series', 'Number 5s', 'Seat'])
print(most_fives)
print(least_fives)


#Highest and lowest episode scores per seat

episode_scores = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[1:7]

    episodes = data[data['Task Number'].str.contains(r'Ep', na = False)].reset_index(drop = True)

    episodes['Description'] = episodes['Description'].str.replace(" Total", "", regex=False)

    episodes = episodes[contestents]
    
    episodes['Series'] = f'S{series}'

    episode_scores.append(episodes)

episode_scores = pd.DataFrame(np.vstack(episode_scores), columns = ['Episode', 'Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series'])

print(episode_scores)

highest_ep_scores = []
lowest_ep_scores = []
for seat in range(1, 6):
    seat_ep_score = episode_scores[['Series', 'Episode', f'Seat {seat}']]

    highest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
    highest_ep['Seat'] = f'Seat {seat}'
    highest_ep_scores.append(highest_ep)

    lowest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
    lowest_ep['Seat'] = f'Seat {seat}'
    lowest_ep_scores.append(lowest_ep)

highest_ep_scores = pd.DataFrame(np.vstack(highest_ep_scores) , columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)
lowest_ep_scores = pd.DataFrame(np.vstack(lowest_ep_scores), columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)

print(highest_ep_scores)
print(lowest_ep_scores)

named_series_table_reformatted = named_series_table.melt(id_vars= 'Series', var_name = 'Seat', value_name = 'Name')
named_series_table_reformatted['Seat'] = named_series_table_reformatted['Seat'].str.replace(' Name', "")
print(named_series_table_reformatted.head())

highest_ep_scores = pd.merge(left = highest_ep_scores, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left')

lowest_ep_scores = pd.merge(left = lowest_ep_scores, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left')

print(highest_ep_scores.head())