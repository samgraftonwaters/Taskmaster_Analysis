import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import Further_Scores_Functions as FSF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv')
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)

print(gender_age_table.head())

gender_count = gender_age_table['Gender'].value_counts().reset_index()

gender_count.columns = ['Gender', 'Count']

gender_count['Percent'] = (gender_count['Count'] / gender_count['Count'].sum() ) * 100
print(gender_count)

gender_series = gender_age_table.groupby('Series Number')['Gender'].value_counts().reset_index()
gender_series = gender_series.sort_values('Series Number', ascending = True)
print(gender_series)


gender_series.plot(kind='bar', x = 'Series Number', y = 'count', figsize=(6,4))
plt.title('Gender counts per series')
plt.xlabel('Series')
plt.ylabel('Count')
plt.xticks(rotation=0)  # keep x labels horizontal
plt.legend(title='Gender')
plt.show()

gender_series_plot = gender_age_table.groupby(['Series Number', 'Gender']).size().unstack(fill_value=0)
print(gender_series_plot)

nb_row = gender_series_plot[gender_series_plot['Non-Binary'] == 1]
print(nb_row)

series = gender_series_plot.index
genders = gender_series_plot.columns
x = np.arange(len(series))  # the label locations
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(6,4))

# Plot Male and Female bars side by side
ax.bar(x - width/2, gender_series_plot['Male'], width, label='Male', color='skyblue')
ax.bar(x + width/2, gender_series_plot['Female'], width, label='Female', color='lightpink')
ax.scatter(
    x[gender_series_plot['Non-Binary'] == 1],
    gender_series_plot.loc[gender_series_plot['Non-Binary'] == 1, 'Non-Binary'],
    color='red',
    marker='D',
    s=100,
    label='Non-Binary (present)'
)

# Labels, title, ticks
ax.set_xlabel('Series')
ax.set_ylabel('Count')
ax.set_ylim(0, 6)
ax.set_title('Counts of Male and Female per Series')
ax.set_xticks(x)
ax.set_xticklabels(series)
ax.legend()

plt.show()

