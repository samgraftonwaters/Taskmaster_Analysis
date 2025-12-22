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
tie_break_scores = []
before_tie_total = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    cols = data.columns

    contestents = cols[2:9]

    episodes = data[data['Task Number'].str.contains(r'Ep', na = False)].reset_index(drop = True)

    tie_breaks = data[data['Task Number'] == 'T'].reset_index(drop = True)

    episodes = episodes[contestents]
    tie_breaks  = tie_breaks[contestents]

    episodes['Episode'] = episodes['Episode'].str.replace(" Total", "", regex=False)
    episodes = episodes.drop('Tasknumber', axis = 1).reset_index(drop = True)
    tie_breaks = tie_breaks.drop('Tasknumber', axis = 1).reset_index(drop = True)
    episodes_with_tie = episodes.copy()


    episodes[episodes.columns[0:5]] = (
    episodes.set_index("Episode")[episodes.columns[0:5]]
    .add(
        tie_breaks.set_index("Episode")[tie_breaks.columns[0:5]],
        fill_value=0
    ).values)

    episodes['Series'] = f'S{series}'
    tie_breaks['Series'] = f'S{series}'
    episodes_with_tie['Series'] = f'S{series}'
    print(episodes_with_tie)

    episode_scores.append(episodes)
    tie_break_scores.append(tie_breaks)
    before_tie_total.append(episodes_with_tie)

episode_scores = pd.DataFrame(np.vstack(episode_scores), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])
tie_break_scores = pd.DataFrame(np.vstack(tie_break_scores), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])

print('hello')
print(episode_scores.head())
print()
print()

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
    plt.text(score+0.1, i, int(score), fontsize = 15, color = 'black')


# plt.yticks(highest_ep_scores['index']-1, highest_ep_scores['Series'], fontsize = 14)
plt.yticks([],[])

plt.xticks(fontsize = 14)
plt.xlim(0, highest_ep_scores['Score'].max() + 2)
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
    plt.text(score+0.1, i, int(score), fontsize = 15, color = 'black')


# plt.yticks(lowest_ep_scores['index'] - 1, lowest_ep_scores['Series'], fontsize = 14)
plt.yticks([],[])
plt.xticks(fontsize = 14)
plt.xlim(0, lowest_ep_scores['Score'].max() + 0.5)
plt.xlabel('Episode Score', fontsize = 18)
plt.ylabel('', fontsize = 18)
# plt.ylabel('Series', fontsize = 18)

plt.title('Lowest Total Scores in an Episode per Seat', fontsize = 20)

plt.show()

print(episode_scores.head(20))

#Number of times each contestent (seat) has one or lost an episode in each series

seat_cols = [c for c in episode_scores.columns if c.startswith("Seat")]

episode_win_lose = episode_scores.melt(
    id_vars=["Episode", "Series"],
    value_vars=seat_cols,
    var_name="Seat",
    value_name="Score"
)

episode_win_lose["max_score"] = episode_win_lose.groupby(["Series", "Episode"])["Score"].transform("max")
episode_win_lose["min_score"] = episode_win_lose.groupby(["Series", "Episode"])["Score"].transform("min")

episode_win_lose["Win"]  = episode_win_lose["Score"] == episode_win_lose["max_score"]
episode_win_lose["Loss"] = episode_win_lose["Score"] == episode_win_lose["min_score"]

episode_win_lose["Number_Episodes"] = episode_win_lose.groupby("Series")["Episode"].transform("count")

episode_win_lose_results = (
    episode_win_lose.groupby(["Series", "Seat"])
    .agg(
        Wins=("Win", "sum"),
        Losses=("Loss", "sum"),
        Number_Episodes=("Episode", "nunique")
    )
    .reset_index()
)

print(episode_win_lose_results.head())
episode_win_lose_results["Series_num"] = episode_win_lose_results["Series"].str.extract(r"(\d+)").astype(int)

episode_win_lose_results = episode_win_lose_results.sort_values("Series_num").drop(columns="Series_num")

episode_win_lose_results = pd.merge(left = episode_win_lose_results, right = named_series_table_reformatted,
                                    on = ['Series', 'Seat'], how = 'left')

episode_win_lose_results['Percentage_Won'] = round((episode_win_lose_results ['Wins'] / episode_win_lose_results ['Number_Episodes']), 2)
episode_win_lose_results['Percentage_Lost'] = round((episode_win_lose_results ['Losses'] / episode_win_lose_results ['Number_Episodes']), 2)

most_eps_won_num = episode_win_lose_results[['Series', 'Seat', "Wins", 'Percentage_Won', 'Number_Episodes', 'Name']].sort_values(by = 'Wins', ascending = False).reset_index(drop = True)

most_eps_lost_num = episode_win_lose_results[['Series', 'Seat', "Losses", 'Percentage_Lost', 'Number_Episodes', 'Name']].sort_values(by = 'Losses', ascending = False).reset_index(drop = True)

most_eps_won_percent = episode_win_lose_results[['Series', 'Seat', "Wins", 'Percentage_Won', 'Number_Episodes', 'Name']].sort_values(by = 'Percentage_Won', ascending = False).reset_index(drop = True)

most_eps_lost_percent = episode_win_lose_results[['Series', 'Seat', "Losses", 'Percentage_Lost', 'Number_Episodes', 'Name']].sort_values(by = 'Percentage_Lost', ascending = False).reset_index(drop = True)

most_eps_won_percent_top = most_eps_won_percent[0:10].sort_values(by = 'Percentage_Won', ascending = True).reset_index(drop = True)
most_eps_lost_percent_top = most_eps_lost_percent[0:10].sort_values(by = 'Percentage_Lost', ascending = True).reset_index(drop = True)


never_won = most_eps_won_percent.sort_values(by = 'Percentage_Won', ascending = True).reset_index(drop = True)
never_lost = most_eps_lost_percent.sort_values(by = 'Percentage_Lost', ascending = True).reset_index(drop = True)

print(most_eps_won_num.head(10))
print(most_eps_lost_num.head(10))

print(most_eps_won_percent.head(10))
print(most_eps_lost_percent.head(10))

# Contestents who never won or never lost an episode
print(never_won.head(10))
print(never_lost.head(20))

fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, sharex = True)
plt.subplots_adjust(wspace=0, hspace=0.05, bottom=0.1, top=0.94, left=0.02, right=0.98)

most_eps_won_percent_top.plot.barh(y='Percentage_Won', x='Name', ax=ax1, color='red', alpha=0.8, 
                 edgecolor='white', width=0.9, label='Most Episodes Won')

for i, (wins, percent, number, name, series, seat) in enumerate(zip(most_eps_won_percent_top['Wins'], 
                                                                    most_eps_won_percent_top['Percentage_Won'],
                                            most_eps_won_percent_top['Number_Episodes'], 
                                              most_eps_won_percent_top['Name'],
                                              most_eps_won_percent_top['Series'],
                                              most_eps_won_percent_top['Seat'])):
    
    
    ax1.text(-0.29, i, series, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.2, i, wins, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.15, i, number, va='center', ha='left', fontsize=12, color='black')
    ax1.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    ax1.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
    ax1.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'red')
    ax1.text(-0.29, 10, 'Series  Number  Episodes', fontsize = 12, color = 'black')

ax1.set_xlim(-0.30, 0.85)
ax1.set_yticks([])
ax1.set_ylabel('')
ax1.legend(fontsize=15)

most_eps_lost_percent_top.plot.barh(y='Percentage_Lost', x='Name', ax=ax2, color='dodgerblue', alpha=0.7,
                 edgecolor='white', width=0.9, label='Most Episodes Lost')

for i, (losses, percent, number, name, series, seat) in enumerate(zip(most_eps_lost_percent_top['Losses'], most_eps_lost_percent_top['Percentage_Lost'],
                                              most_eps_lost_percent_top['Number_Episodes'], 
                                              most_eps_lost_percent_top['Name'],
                                              most_eps_lost_percent_top['Series'],
                                              most_eps_lost_percent_top['Seat'])):

    ax2.text(-0.29, i, series, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.2, i, wins, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.15, i, number, va='center', ha='left', fontsize=12, color='black')
    ax2.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    ax2.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'black')
    ax2.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'blue')
    # ax2.text(-0.29, 10, 'Series  Number  Episodes  Seat', fontsize = 11, color = 'black')

ax2.set_xlim(-0.30, 0.85)
ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
ax2.set_yticks([])
ax2.set_ylabel('')
ax2.legend(fontsize=15)

fig.suptitle("Proportion of Times Contestents Won or Lost each Episode", fontsize = 18)
plt.xlabel('Proportion', fontsize=18)
plt.ylabel('')
ax1.tick_params(axis='x', labelsize=12)
ax2.tick_params(axis='x', labelsize=14)

plt.show()


## Tie Breaks
print('Tie Break Analysis\n\n\n')

before_tie_total = pd.DataFrame(np.vstack(before_tie_total), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])

tie_break_scores = tie_break_scores.merge(
    before_tie_total,
    on=["Series", "Episode"],
    suffixes=("_tb", "_score")
)

seat_cols = [f"Seat {i}" for i in range(1, 6)]

rows = []

for _, row in tie_break_scores.iterrows():
    series = row["Series"]
    episode = row["Episode"]

    # scores per seat
    scores = {seat: row[f"{seat}_score"] for seat in seat_cols}

    # find tied scores (appearing more than once)
    score_counts = pd.Series(scores).value_counts()
    tied_scores = score_counts[score_counts > 1].index 

    for tied_score in tied_scores:
        tied_seats = [seat for seat, tie in scores.items() if tie == tied_score]

        winners = [seat for seat in tied_seats if row[f"{seat}_tb"] == 1]
        losers  = [seat for seat in tied_seats if row[f"{seat}_tb"] == 0]

        # create all winner–loser combinations
        for win in winners:
            for lost in losers:
                rows.append({
                    "Series": series,
                    "Episode": episode,
                    "Seat Winner": win,
                    "Seat Loser": lost})

tie_break_scores = pd.DataFrame(rows)

tie_break_scores_names = (
    tie_break_scores
    .merge(
    named_series_table_reformatted,
        left_on=["Series", "Seat Winner"],
        right_on=["Series", "Seat"],
        how="left"
    )
    .rename(columns={"Name": "Seat Winner Name"})
    .drop(columns="Seat")
)

tie_break_scores_names = (
    tie_break_scores_names
    .merge(
        named_series_table_reformatted,
        left_on=["Series", "Seat Loser"],
        right_on=["Series", "Seat"],
        how="left"
    )
    .rename(columns={"Name": "Seat Loser Name"})
    .drop(columns="Seat")
)

tie_break_scores_names["Tie breaks per series"] = (
    tie_break_scores_names.groupby("Series")["Episode"]
    .transform("nunique")
)

tie_break_scores_names["Tie break Wins per Person"] = (
    tie_break_scores_names.groupby("Series")["Seat Winner Name"]
    .transform("count")
)

tie_break_scores_names["Tie break Losses per Person"] = (
    tie_break_scores_names.groupby("Series")["Seat Loser Name"]
    .transform("count")
)

tie_break_scores_names= tie_break_scores_names[["Series", "Episode", "Seat Winner",
        "Seat Winner Name", "Seat Loser", "Seat Loser Name", "Tie break Wins per Person", 
        'Tie break Losses per Person', "Tie breaks per series"]]

print(tie_break_scores_names.head(20))

count_winners = (tie_break_scores_names[["Series","Seat Winner Name", "Tie break Wins per Person",
                                        "Tie breaks per series"]]
      .rename(columns={"Seat Winner Name": "Name"})
      .assign(Wins=1)
      .groupby(["Series", "Name", "Tie breaks per series", "Tie break Wins per Person"], 
               as_index=False)["Wins"].sum())

count_losers = (tie_break_scores_names[["Series", "Seat Loser Name", 'Tie break Losses per Person',
                                        "Tie breaks per series"]]
      .rename(columns={"Seat Loser Name": "Name"})
      .assign(Losses=1)
      .groupby(["Series", "Name", "Tie breaks per series", 'Tie break Losses per Person'],as_index=False)["Losses"].sum())

count_winners_losers = (
    pd.concat([
        count_winners.rename(columns={"Wins": "Count"}).assign(Result="Win"),
        count_losers.rename(columns={"Losses": "Count"}).assign(Result="Loss")
    ]).sort_values(["Series", "Name"]).reset_index(drop=True))

count_winners_losers = count_winners_losers.replace(np.nan, 0)

count_winners['Percentage Wins'] = round((count_winners["Wins"] / count_winners['Tie break Wins per Person']),2)
count_losers['Percentage Losses'] = round((count_losers["Losses"] / count_losers['Tie break Losses per Person']),2)

top_count_winners = count_winners.sort_values(by = ['Percentage Wins', 'Wins'], ascending = False).reset_index(drop = True)
top_count_losers = count_losers.sort_values(by = ['Percentage Losses', 'Losses'], ascending = False).reset_index(drop = True)

print(count_winners.head(20))
print(count_losers.head(20))
print(count_winners_losers.head(20))

print(top_count_winners.head(20))
print(top_count_losers.head(20))