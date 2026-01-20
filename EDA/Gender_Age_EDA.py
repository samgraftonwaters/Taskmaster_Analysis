import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import gender_age_functions as GAF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

episode_scores = pd.read_csv(file_path + 'Episode Wins and Losses.csv')
final_scores = pd.read_csv(file_path + 'Total Final Scores and Positions.csv')

print(episode_scores.head())
print(final_scores.head())

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv')
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)
print(gender_age_table.columns)

gender_count = GAF.gender_count_percent(gender_age_table)
gender_series = GAF.gender_count_series(gender_age_table)
GAF.gender_count_series_bar(gender_age_table)

age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_table = age_table.copy()
print(age_table)

age_bins = [20, 30, 40, 50, 60, 70]
age_labels = ['20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69']

age_table['Age_Ranges'] = pd.cut(age_table['Age_at_First_Air'], bins = age_bins, labels = age_labels, right = False)

age_ranges_count = age_table['Age_Ranges'].value_counts().reset_index()
age_ranges_count.columns = ['Age_Ranges', 'Count']
age_ranges_count['Percentage'] = (age_ranges_count['Count'] / age_ranges_count['Count'].sum()) * 100
print(age_ranges_count)

age_series = age_table.groupby('Series Number')['Age_Ranges'].value_counts().reset_index()
age_series = age_series.sort_values('Series Number', ascending = True)

age_series_plot = age_series.pivot_table(index="Series Number", columns="Age_Ranges", values="count",
        aggfunc="sum", fill_value=0).reset_index()

print(age_series_plot)


x_pos = [-1.5, -0.75, 0, 0.75, 1.5]
colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)
for i, (bins, pos, colour) in enumerate(zip(age_labels, x_pos, colours)):
    
#     age = age_series[age_series['Age_Ranges'] == bins].reset_index(drop = True)
#     plt.bar(age['Series Number'] + pos, age['count'], width = 0.1, edgecolor = 'black', color = colour, label = bins)
    plt.bar(age_series_plot['Series Number'] + pos, age_series_plot[bins], width = 0.1, edgecolor = 'black', color = colour, label = bins)

plt.xlim(0, 21)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.legend()
plt.show()

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96) 
ax = age_series_plot.plot(x='Series Number', kind='bar', stacked=True, width = 0.8, ax = ax)

ax.tick_params(axis='x', labelrotation=0)

for c in ax.containers:
    labels = [f"{int(v.get_height())}"
        if np.isfinite(v.get_height()) and v.get_height() > 0 else '' for v in c]
    
    ax.bar_label(c, labels=labels, label_type='center', color = 'white', fontsize = 12)

plt.xlabel("Series", fontsize = 20)
plt.ylabel("Count", fontsize = 20)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.legend(fontsize = 15)
plt.title('Number of Age Ranges for each Contestent per Series', fontsize = 22)
plt.show()

x = age_series_plot['Series Number'] 

plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)
plt.bar(x, age_series_plot['20 - 29'], color = colours[0], label = age_labels[0])
plt.bar(x, age_series_plot['30 - 39'], bottom = age_series_plot['20 - 29'], color = colours[1], label = age_labels[1])
plt.bar(x, age_series_plot['40 - 49'], bottom=age_series_plot['20 - 29']+age_series_plot['30 - 39'], color = colours[2], label = age_labels[2])
plt.bar(x, age_series_plot['50 - 59'], bottom=age_series_plot['20 - 29']+age_series_plot['30 - 39']+age_series_plot['40 - 49'], color = colours[3], label = age_labels[3])
plt.bar(x, age_series_plot['60 - 69'], bottom=age_series_plot['20 - 29']+age_series_plot['30 - 39']+age_series_plot['40 - 49']+age_series_plot['50 - 59'], color = colours[4], label = age_labels[4])
plt.xlabel("Series", fontsize = 18)
plt.ylabel("Count", fontsize = 18)
plt.xlim(0.5, 20.5)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.legend(fontsize = 12)
plt.title("Scores by Teams in 4 Rounds")

    

age_series_plot = age_series.groupby(['Series Number', 'Age_Ranges']).size().unstack(fill_value=0)
# print(age_series_plot)
series = age_series_plot.index
x = np.arange(len(series))+1 
#Percentage differnce bar charts for four team score methods
plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.96)

plt.bar(x-0.3, age_series_plot['20 - 29'], 
        width = 0.2, edgecolor = 'black', label = 'Total Team Score')
plt.bar(x-0.1, age_series_plot['30 - 39'], 
        width = 0.2, edgecolor = 'black', label = 'Team Score per Person')
plt.bar(x+0.1, age_series_plot['40 - 49'], 
        width = 0.2, edgecolor = 'black', label = 'Team Score per Task')
plt.bar(x+0.3, age_series_plot['50 - 59'], 
        width = 0.2, edgecolor = 'black', label = 'Score per Person per Task')
plt.xlim(0.5, 20.5)
plt.ylim(0, 5)
plt.xticks(np.arange(1, 21, 1), fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlabel('Series', fontsize = 20)
plt.ylabel('Absolute Percentage Differences', fontsize = 20)
plt.title('Absolute Percentage Differences between Team of Three and Team \n of Two for Four Different Team Score Methods',
          fontsize = 18)
plt.legend(loc = 'upper right', fontsize = 16, ncol = 2)
# plt.show()
