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

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.88, left = 0.08, right = 0.96) 
ax = age_series_plot.plot(x='Series Number', kind='bar', stacked=True, width = 0.8, ax = ax)

plt.text(0.05, 5.33, 'Age Ranges:', fontsize = 14)

for c in ax.containers:
    labels = [f"{int(v.get_height())}"
        if np.isfinite(v.get_height()) and v.get_height() > 0 else '' for v in c]
    
    ax.bar_label(c, labels=labels, label_type='center', color = 'white', fontsize = 14)

ax.tick_params(axis='x', labelrotation=0)
plt.xlabel("Series", fontsize = 20)
plt.ylabel("Count", fontsize = 20)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)

ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=5, fontsize=14, frameon=False)
plt.title('Number of Age Ranges for each Contestent per Series', pad=30, fontsize = 24)
plt.show()