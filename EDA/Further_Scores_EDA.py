import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

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

    diff_scores = (final_scores.max(axis=1) - final_scores.min(axis = 1)).astype(int)

    score_diff.append([diff_scores.values[0], f'S{series}'])

score_diff = pd.DataFrame(score_diff, columns = ['Difference', 'Series'])

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

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


#Reformating contestents table to merge with the next methods below:

named_series_table_reformatted = named_series_table.melt(id_vars= 'Series', var_name = 'Seat', value_name = 'Name')
named_series_table_reformatted['Seat'] = named_series_table_reformatted['Seat'].str.replace(' Name', "")


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

# print(count_one)
# print(count_five)

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

most_ones = pd.DataFrame(np.vstack(most_ones), columns = ['Series', 'Most 1s', 'Seat'])
least_ones = pd.DataFrame(np.vstack(least_ones), columns = ['Series', 'Least 1s', 'Seat'])

most_ones = pd.merge(left = most_ones, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Most 1s', ascending = False).reset_index(drop = True)

most_ones['index'] = most_ones.index.values + 1

least_ones = pd.merge(left = least_ones, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Least 1s', ascending = False).reset_index(drop = True)

least_ones['index'] = least_ones.index.values + 1

most_fives = pd.DataFrame(np.vstack(most_fives), columns = ['Series', 'Most 5s', 'Seat'])
least_fives = pd.DataFrame(np.vstack(least_fives), columns = ['Series', 'Least 5s', 'Seat'])

most_fives = pd.merge(left = most_fives, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Most 5s', ascending = False).reset_index(drop = True)

most_fives['index'] = most_fives.index.values + 1

least_fives = pd.merge(left = least_fives, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Least 5s', ascending = False).reset_index(drop = True)

least_fives['index'] = least_fives.index.values + 1

# print(most_ones)
# print(least_ones)

fig, (ax1, ax2) = plt.subplots(ncols = 1, nrows = 2, sharex = True)
plt.subplots_adjust(wspace=0, hspace=0.05, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

sns.barplot(most_ones, x="Most 1s", y="index", orient="y", hue = 'Seat', legend = False, ax = ax1)

for i, (score, name, series, seat) in enumerate(zip(most_ones['Most 1s'], most_ones['Name'],
                                              most_ones['Series'], most_ones['Seat'])):
    ax1.text(4.2, i, name, va='center', ha='left', fontsize=15, color='white')
    ax1.text(8.1, i, series, va='center', ha='left', fontsize=15, color='white')
    ax1.text(9, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    ax1.text(score+0.1, i, score, fontsize = 15, color = 'black')
    

sns.barplot(least_ones, x="Least 1s", y="index", orient="y", hue = 'Seat', legend = False, ax = ax2)

for i, (score, name, series, seat) in enumerate(zip(least_ones['Least 1s'], least_ones['Name'],
                                              least_ones['Series'], least_ones['Seat'])):
    ax2.text(5, i, name, va='center', ha='left', fontsize=15, color='black')
    ax2.text(8, i, series, va='center', ha='left', fontsize=15, color='black')
    ax2.text(9, i, seat, va='center', ha='left', fontsize=15, color = 'black')
    ax2.text(score+0.1, i, score, fontsize = 15, color = 'black')

ax1.text(16, 5, 'Most 1s', fontsize = 20, color = 'black')
ax2.text(16, 5, 'Least 1s', fontsize = 20, color = 'black')

ax1.set_yticks([],[])
ax2.set_yticks([],[])
ax1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
ax2.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
ax2.tick_params(axis = 'x', labelsize = 14)
ax1.set_ylabel('')
ax2.set_ylabel('')
ax2.set_xlabel('')
plt.suptitle('Most and Least Number of 1s Scored Per Seat', fontsize = 20)
plt.show()

# print(most_fives)
# print(least_fives)

fig, (ax1, ax2) = plt.subplots(ncols = 1, nrows = 2, sharex = True)
plt.subplots_adjust(wspace=0, hspace=0.05, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

sns.barplot(most_fives, x="Most 5s", y="index", orient="y", hue = 'Seat', legend = False, ax = ax1)

for i, (score, name, series, seat) in enumerate(zip(most_fives['Most 5s'], most_fives['Name'],
                                              most_fives['Series'], most_fives['Seat'])):
    ax1.text(5, i, name, va='center', ha='left', fontsize=15, color='white')
    ax1.text(9, i, series, va='center', ha='left', fontsize=15, color='white')
    ax1.text(10.5, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    ax1.text(score+0.1, i, score, fontsize = 15, color = 'black')

sns.barplot(least_fives, x="Least 5s", y="index", orient="y", hue = 'Seat', legend = False, ax = ax2)

for i, (score, name, series, seat) in enumerate(zip(least_fives['Least 5s'], least_fives['Name'],
                                              least_fives['Series'], least_fives['Seat'])):
    ax2.text(5, i, name, va='center', ha='left', fontsize=15, color='black')
    ax2.text(9, i, series, va='center', ha='left', fontsize=15, color='black')
    ax2.text(10.5, i, seat, va='center', ha='left', fontsize=15, color = 'black')
    ax2.text(score+0.1, i, score, fontsize = 15, color = 'black')

ax1.text(18.5, 4, 'Most 5s', fontsize = 20, color = 'black')
ax2.text(18.5, 5, 'Least 5s', fontsize = 20, color = 'black')

ax1.set_yticks([],[])
ax2.set_yticks([],[])
ax1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
ax2.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
ax2.tick_params(axis = 'x', labelsize = 14)
ax1.set_ylabel('')
ax2.set_ylabel('')
ax2.set_xlabel('')
plt.suptitle('Most and Least Number of 5s Scored Per Seat', fontsize = 20)
plt.show()

#Highest and lowest episode scores per seat

episode_scores = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[2:9]

    episodes = data[data['Task Number'].str.contains(r'Ep', na = False)].reset_index(drop = True)

    tie_breaks = data[data['Task Number'] == 'T'].reset_index(drop = True)


    episodes = episodes[contestents]
    tie_breaks  = tie_breaks[contestents]

    episodes['Episode'] = episodes['Episode'].str.replace(" Total", "", regex=False)
    episodes = episodes.drop('Tasknumber', axis = 1)
    tie_breaks = tie_breaks.drop('Tasknumber', axis = 1)

    episodes[episodes.columns[0:5]] = (
    episodes.set_index("Episode")[episodes.columns[0:5]]
    .add(
        tie_breaks.set_index("Episode")[tie_breaks.columns[0:5]],
        fill_value=0
    )
    .values)

    episodes['Series'] = f'S{series}'

    episode_scores.append(episodes)


episode_scores = pd.DataFrame(np.vstack(episode_scores), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])

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


highest_ep_scores = pd.merge(left = highest_ep_scores, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = False).reset_index(drop = True)

highest_ep_scores['index'] = highest_ep_scores.index.values + 1

lowest_ep_scores = pd.merge(left = lowest_ep_scores, right = named_series_table_reformatted, 
                             on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = True).reset_index(drop = True)

lowest_ep_scores['index'] = lowest_ep_scores.index.values + 1


# print(highest_ep_scores)
# print(lowest_ep_scores)


plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

# plt.barh(highest_ep_scores['index'], highest_ep_scores['Score'], color='red', alpha=0.8, 
#                  edgecolor='white', label='Top Ten Teams')

sns.barplot(highest_ep_scores, x="Score", y="index", orient="y", hue = 'Seat', legend = False)

for i, (score, name, series, episode, seat) in enumerate(zip(highest_ep_scores['Score'], highest_ep_scores['Name'],
                                              highest_ep_scores['Series'], highest_ep_scores['Episodes'],
                                              highest_ep_scores['Seat'])):
    plt.text(1, i, name, va='center', ha='left', fontsize=15, color='white')
    plt.text(12, i, series, va='center', ha='left', fontsize=15, color='white')
    plt.text(15, i, episode, va='center', ha='left', fontsize=15, color='white')
    plt.text(18, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    plt.text(score+0.1, i, score, fontsize = 15, color = 'black')


# plt.yticks(highest_ep_scores['index']-1, highest_ep_scores['Series'], fontsize = 14)
plt.yticks([],[])

plt.xticks(fontsize = 14)
plt.xlim(0, highest_ep_scores['Score'].max() + 1)
plt.xlabel('Episode Score', fontsize = 18)
# plt.ylabel('Series', fontsize = 18)
plt.ylabel('', fontsize = 18)

plt.title('Highest Total Scores in an Episode per Seat', fontsize = 20)

plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

# plt.barh(lowest_ep_scores['index'], lowest_ep_scores['Score'], color='dodgerblue', alpha=0.8, 
#                  edgecolor='white', label='Top Ten Teams')

sns.barplot(lowest_ep_scores, x="Score", y="index", orient="y", hue = 'Seat', legend = False)

for i, (score, name, series, episode, seat) in enumerate(zip(lowest_ep_scores['Score'], lowest_ep_scores['Name'],
                                              lowest_ep_scores['Series'], lowest_ep_scores['Episodes'],
                                              lowest_ep_scores['Seat'])):
    plt.text(0.25, i, name, va='center', ha='left', fontsize=15, color='white')
    plt.text(1.5, i, series, va='center', ha='left', fontsize=15, color='white')
    plt.text(2, i, episode, va='center', ha='left', fontsize=15, color='white')
    plt.text(2.4, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    plt.text(score+0.1, i, score, fontsize = 15, color = 'black')


# plt.yticks(lowest_ep_scores['index'] - 1, lowest_ep_scores['Series'], fontsize = 14)
plt.yticks([],[])
plt.xticks(fontsize = 14)
plt.xlim(0, lowest_ep_scores['Score'].max() + 1)
plt.xlabel('Episode Score', fontsize = 18)
plt.ylabel('', fontsize = 18)
# plt.ylabel('Series', fontsize = 18)

plt.title('Lowest Total Scores in an Episode per Seat', fontsize = 20)

plt.show()

print(episode_scores.head(20))

for series in range(1,21):

    most_ep_wins = episode_scores[episode_scores['Series'] == f'S{series}']