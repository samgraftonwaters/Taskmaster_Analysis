import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import Further_Scores_Functions as FSF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

scores_series_table = file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')

named_series_table_reformatted = named_series_table.melt(id_vars= 'Series', var_name = 'Seat', value_name = 'Name')
named_series_table_reformatted['Seat'] = named_series_table_reformatted['Seat'].str.replace(' Name', "")


score_diff = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')
    cols = data.columns
    contestents = cols[2:7]

    #Finding difference between max and min scores
    final_scores = data[data['Task Number'] == f'Series {series} Grand Total'].reset_index(drop = True)
    final_scores = final_scores[contestents]
    diff_scores = (final_scores.max(axis=1) - final_scores.min(axis = 1)).astype(int)
    score_diff.append([diff_scores.values[0], f'S{series}'])

score_diff = pd.DataFrame(score_diff, columns = ['Difference', 'Series'])

#Number of times contestents got e.g. 1 or 5 points.
#Then finds the most and least for each points category for each seat

count_one = FSF.count_scores(dataframe = scores_series_table, score = 1)
count_five = FSF.count_scores(dataframe = scores_series_table, score = 5)

most_ones = FSF.most_least_scores(count_scores = count_one, named_table = named_series_table_reformatted, 
                                  score = 1, size = 'most')
least_ones = FSF.most_least_scores(count_scores = count_one, named_table = named_series_table_reformatted, 
                                   score = 1, size = 'least')

most_fives = FSF.most_least_scores(count_scores = count_five, named_table = named_series_table_reformatted, 
                                   score = 5, size = 'most')
least_fives = FSF.most_least_scores(count_scores = count_five, named_table = named_series_table_reformatted, 
                                    score = 5, size = 'least')

#Highest and lowest episode scores per seat

episode_scores, tie_break_scores, before_tie_total = FSF.episode_tie_scores(data_table = scores_series_table)

lowest_ep_scores = FSF.high_low_ep_scores(data_table = episode_scores, named_table = named_series_table_reformatted, 
                       direction = 'lowest')

highest_ep_scores = FSF.high_low_ep_scores(data_table = episode_scores, named_table = named_series_table_reformatted, 
                       direction = 'highest')


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

## Tie Breaks
print('Tie Break Analysis\n\n\n')

(tie_break_count_winners, tie_break_count_losers, 
 tie_break_count_winners_losers, tie_break_scores_names) = FSF.tie_break_calcs(tie_break_scores_table = tie_break_scores, 
                                                                                                      before_tie_total_table = before_tie_total, 
                                                                                                      named_table = named_series_table_reformatted)
print(tie_break_scores_names.head(20))

tie_break_count_winners["Tie breaks per series"] = tie_break_count_winners["Tie breaks per series"] - tie_break_count_winners["Double Losers"]

tie_break_count_losers["Tie breaks per series"] = tie_break_count_losers["Tie breaks per series"] - tie_break_count_losers["Double Losers"]

tie_break_count_winners['Wins'] = round((tie_break_count_winners["Wins"] - tie_break_count_winners["Double Losers"]),2)
tie_break_count_losers['Losses'] = round((tie_break_count_losers["Losses"] - tie_break_count_losers["Double Losers"]),2)

tie_break_count_winners['Percentage Wins Series'] = round((tie_break_count_winners["Wins"] / tie_break_count_winners['Tie breaks per series']),2)
tie_break_count_losers['Percentage Losses Series'] = round((tie_break_count_losers["Losses"] / tie_break_count_losers['Tie breaks per series']),2)

tie_break_count_winners['Percentage Wins Person'] = round((tie_break_count_winners["Wins"] / tie_break_count_winners['Tie Breaks per Person']),2)
tie_break_count_losers['Percentage Losses Person'] = round((tie_break_count_losers["Losses"] / tie_break_count_losers['Tie Breaks per Person']),2)

top_tie_break_count_winners = tie_break_count_winners.sort_values(by = ['Percentage Wins Person', 'Wins'], ascending = False).reset_index(drop = True)
top_tie_break_count_losers = tie_break_count_losers.sort_values(by = ['Percentage Losses Person', 'Losses'], ascending = False).reset_index(drop = True)

seat_winners = top_tie_break_count_winners[['Seat', 'Wins', 'Tie breaks per series']]
seat_losers = top_tie_break_count_losers[['Seat', 'Losses', 'Tie breaks per series']]

print(top_tie_break_count_winners.head(50))
print(top_tie_break_count_losers.head(50))

#Tie break count number of winners and losers

top_tie_break_count_winners = top_tie_break_count_winners[0:19].sort_values(by = ['Percentage Wins Person', 'Wins'], ascending = True).reset_index(drop = True)
top_tie_break_count_losers = top_tie_break_count_losers[0:19].sort_values(by = ['Percentage Losses Person', 'Losses'], ascending = True).reset_index(drop = True)

top_tie_break_count_winners = top_tie_break_count_winners[0:19].sort_values(by = ['Percentage Wins Series', 'Wins'], ascending = True).reset_index(drop = True)
top_tie_break_count_losers = top_tie_break_count_losers[0:19].sort_values(by = ['Percentage Losses Series', 'Losses'], ascending = True).reset_index(drop = True)

seat_winners_totals = seat_winners.groupby('Seat')[['Wins', 'Tie breaks per series']].sum().reset_index()
seat_losers_totals = seat_losers.groupby('Seat')[['Losses', 'Tie breaks per series']].sum().reset_index()

seat_winners_totals['Percentage Wins per Seat'] = seat_winners_totals['Wins']/seat_winners_totals['Tie breaks per series']
seat_losers_totals['Percentage Losses per Seat'] = seat_losers_totals['Losses']/seat_losers_totals['Tie breaks per series']

seat_winners_totals['Numbers'] = range(1, 6)
seat_losers_totals['Numbers'] = range(1, 6)

print(seat_winners_totals)
print(seat_losers_totals)


#Plots

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

plt.bar(x = score_diff['Series'], height = score_diff['Difference'], width = 0.8,
        color = 'blue', alpha = 0.7, edgecolor = 'black')

plt.bar(score_diff['Series'][score_diff['Difference'].idxmax(axis = 0)], 
        score_diff['Difference'][score_diff['Difference'].idxmax(axis = 0)], color = 'darkorange',
        edgecolor = 'black', label = 'Biggest Difference')

plt.bar(score_diff['Series'][score_diff['Difference'].idxmin(axis = 0)], 
        score_diff['Difference'][score_diff['Difference'].idxmin(axis = 0)], color = 'maroon',
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

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

sns.barplot(highest_ep_scores, x="Score", y="index", orient="y", hue = 'Seat', legend = False)

for i, (score, name, series, episode, seat) in enumerate(zip(highest_ep_scores['Score'], highest_ep_scores['Name'],
                                              highest_ep_scores['Series'], highest_ep_scores['Episodes'],
                                              highest_ep_scores['Seat'])):
    plt.text(1, i, name, va='center', ha='left', fontsize=15, color='white')
    plt.text(12, i, series, va='center', ha='left', fontsize=15, color='white')
    plt.text(15, i, episode, va='center', ha='left', fontsize=15, color='white')
    plt.text(18, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    plt.text(score+0.1, i, int(score), fontsize = 15, color = 'black')

plt.yticks([],[])

plt.xticks(fontsize = 14)
plt.xlim(0, highest_ep_scores['Score'].max() + 2)
plt.xlabel('Episode Score', fontsize = 18)
plt.ylabel('', fontsize = 18)

plt.title('Highest Total Scores in an Episode per Seat', fontsize = 20)

plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

sns.barplot(lowest_ep_scores, x="Score", y="index", orient="y", hue = 'Seat', legend = False)

for i, (score, name, series, episode, seat) in enumerate(zip(lowest_ep_scores['Score'], lowest_ep_scores['Name'],
                                              lowest_ep_scores['Series'], lowest_ep_scores['Episodes'],
                                              lowest_ep_scores['Seat'])):
    plt.text(0.25, i, name, va='center', ha='left', fontsize=15, color='white')
    plt.text(1.5, i, series, va='center', ha='left', fontsize=15, color='white')
    plt.text(2, i, episode, va='center', ha='left', fontsize=15, color='white')
    plt.text(2.4, i, seat, va='center', ha='left', fontsize=15, color = 'white')
    plt.text(score+0.1, i, int(score), fontsize = 15, color = 'black')

plt.yticks([],[])
plt.xticks(fontsize = 14)
plt.xlim(0, lowest_ep_scores['Score'].max() + 0.5)
plt.xlabel('Episode Score', fontsize = 18)
plt.ylabel('', fontsize = 18)

plt.title('Lowest Total Scores in an Episode per Seat', fontsize = 20)

plt.show()

print(episode_scores.head(20))

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


plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.98)

plt.barh(width=top_tie_break_count_winners['Percentage Wins Person'], y=top_tie_break_count_winners['Name'],
    color='red', alpha=0.8, edgecolor='white', label='Most Tie Breaks Won')

for i, (wins, percent, tie_person, name, series, seat) in enumerate(zip(top_tie_break_count_winners['Wins'], 
                                                                    top_tie_break_count_winners['Percentage Wins Person'],
                                            top_tie_break_count_winners['Tie Breaks per Person'],
                                            top_tie_break_count_winners['Name'],
                                            top_tie_break_count_winners['Series'],
                                            top_tie_break_count_winners['Seat'])):
    
    plt.text(-0.32, i, series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='red')
    plt.text(-0.14, i, tie_person, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    plt.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
    plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'red')
    plt.text(-0.32, 19, 'Series', fontsize = 12, color = 'black')
    plt.text(-0.24, 19, 'Wins', fontsize = 12, color = 'red')
    plt.text(-0.17, 19, '# Ties', fontsize = 12, color = 'black')

plt.xlim(-0.35, 1.1)
plt.ylim(-1, 20)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 18)
plt.yticks([])
plt.ylabel('')
plt.title('Tie Break Percentage Wins per Number for each Person', fontsize = 22)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.98)

plt.barh(width=top_tie_break_count_losers['Percentage Losses Person'], y=top_tie_break_count_losers['Name'],
    color='dodgerblue', alpha=0.8, edgecolor='white', label='Most Tie Breaks Lost')

for i, (wins, percent, tie_person, name, series, seat) in enumerate(zip(top_tie_break_count_losers['Losses'], 
                                                                    top_tie_break_count_losers['Percentage Losses Person'],
                                            top_tie_break_count_losers['Tie Breaks per Person'],
                                            top_tie_break_count_losers['Name'],
                                            top_tie_break_count_losers['Series'],
                                            top_tie_break_count_losers['Seat'])):
    
    plt.text(-0.32, i, series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='blue')
    plt.text(-0.14, i, tie_person, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    plt.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
    plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'blue')
    plt.text(-0.32, 19, 'Series', fontsize = 12, color = 'black')
    plt.text(-0.24, 19, 'Loses', fontsize = 12, color = 'blue')
    plt.text(-0.17, 19, '# Ties', fontsize = 12, color = 'black')

plt.xlim(-0.35, 1.1)
plt.ylim(-1, 20)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 18)
plt.yticks([])
plt.ylabel('')
plt.title('Tie Break Percentage Losses per Number for each Person', fontsize = 22)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.98)

plt.barh(width=top_tie_break_count_winners['Percentage Wins Series'], y=top_tie_break_count_winners['Name'],
    color='red', alpha=0.8, edgecolor='white', label='Most Tie Breaks Won')

for i, (wins, percent, tie_series, name, series, seat) in enumerate(zip(top_tie_break_count_winners['Wins'], 
                                                                    top_tie_break_count_winners['Percentage Wins Series'],
                                            top_tie_break_count_winners['Tie breaks per series'],
                                            top_tie_break_count_winners['Name'],
                                            top_tie_break_count_winners['Series'],
                                            top_tie_break_count_winners['Seat'])):
    
    plt.text(-0.32, i, series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='red')
    plt.text(-0.14, i, tie_series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    plt.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
    plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'red')
    plt.text(-0.32, 19, 'Series', fontsize = 12, color = 'black')
    plt.text(-0.24, 19, 'Wins', fontsize = 12, color = 'red')
    plt.text(-0.17, 19, '# Ties', fontsize = 12, color = 'black')

plt.xlim(-0.35, 1.1)
plt.ylim(-1, 20)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 18)
plt.yticks([])
plt.ylabel('')
plt.title('Tie Break Percentage Wins per Number in each Series', fontsize = 22)
plt.show()

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.98)

plt.barh(width=top_tie_break_count_losers['Percentage Losses Series'], y=top_tie_break_count_losers['Name'],
    color='dodgerblue', alpha=0.8, edgecolor='white', label='Most Tie Breaks Lost')

for i, (wins, percent, tie_series, name, series, seat) in enumerate(zip(top_tie_break_count_losers['Losses'], 
                                                                    top_tie_break_count_losers['Percentage Losses Series'],
                                            top_tie_break_count_losers['Tie breaks per series'],
                                            top_tie_break_count_losers['Name'],
                                            top_tie_break_count_losers['Series'],
                                            top_tie_break_count_losers['Seat'])):
    
    plt.text(-0.32, i, series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='blue')
    plt.text(-0.14, i, tie_series, va='center', ha='left', fontsize=12, color='black')
    plt.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
    plt.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
    plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'blue')
    plt.text(-0.32, 19, 'Series', fontsize = 12, color = 'black')
    plt.text(-0.24, 19, 'Loses', fontsize = 12, color = 'blue')
    plt.text(-0.17, 19, '# Ties', fontsize = 12, color = 'black')

plt.xlim(-0.35, 1.1)
plt.ylim(-1, 20)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 18)
plt.yticks([])
plt.ylabel('')
plt.title('Tie Break Percentage Loses per Number in each Series', fontsize = 22)
plt.show()


fig = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.1, right = 0.95)

plt.bar(x = seat_winners_totals['Numbers']-0.2, height = seat_winners_totals['Percentage Wins per Seat']*100, 
        label = 'Percentage Tie Break Wins', width = 0.40, color = 'blue', alpha = 0.6, edgecolor ='black')
plt.bar(x = seat_losers_totals['Numbers']+0.2, height = seat_losers_totals['Percentage Losses per Seat']*100, 
        label = 'Percentage Tie Break Losses', width = 0.40, color = 'green', alpha = 0.6, edgecolor ='black')


for i in range(len(seat_winners_totals)):
    win_per = seat_winners_totals['Percentage Wins per Seat'][i] * 100
    los_per = seat_losers_totals['Percentage Losses per Seat'][i] * 100
    plt.text(i+0.8, win_per + 2, f"{win_per:.1f}", ha='center', fontsize=15, color='blue')
    plt.text(i+1.2, los_per + 2, f"{los_per:.1f}", ha='center', fontsize=15, color='green')

plt.ylabel('Percentage', fontsize = 20)
plt.yticks(fontsize = 16)
plt.ylim(0, 70)
plt.xticks(fontsize = 16)
plt.xlabel('Seat Number', fontsize = 20)
plt.title('Percentage Win or Lose Rate for each Seat when it comes to Tie Breakers', fontsize = 18)

plt.legend(loc = 'best', fontsize = 15)
plt.show()


fig = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.1, right = 0.95)

plt.bar(x = seat_winners_totals['Numbers']-0.2, height = seat_winners_totals['Wins'], 
        label = 'Number Tie Break Wins', width = 0.40, color = 'blue', alpha = 0.6, edgecolor ='black')
plt.bar(x = seat_losers_totals['Numbers']+0.2, height = seat_losers_totals['Losses'], 
        label = 'Number Tie Break Losses', width = 0.40, color = 'green', alpha = 0.6, edgecolor ='black')

for i in range(len(seat_winners_totals)):
    plt.text(i+0.8, seat_winners_totals['Wins'][i] + 0.75, seat_winners_totals['Wins'][i], ha='center', fontsize=16, color='blue')
    plt.text(i+1.2, seat_losers_totals['Losses'][i] + 0.75, seat_losers_totals['Losses'][i], ha='center', fontsize=16, color='green')

    plt.text(i+0.8, seat_winners_totals['Wins'][i] - 1, seat_winners_totals['Tie breaks per series'][i], ha='center', fontsize=16, color='white')
    plt.text(i+1.2, seat_losers_totals['Losses'][i] - 1, seat_losers_totals['Tie breaks per series'][i], ha='center', fontsize=16, color='white')

plt.ylabel('Count', fontsize = 20)
plt.yticks(fontsize = 16)
plt.ylim(0, 12)
plt.xticks(fontsize = 16)
plt.xlabel('Seat Number', fontsize = 20)
plt.title('Number of Wins or Losses for each Seat when it comes to Tie Breakers', fontsize = 20)

plt.legend(loc = 'best', fontsize = 15)
plt.show()