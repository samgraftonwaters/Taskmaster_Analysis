import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

imdb_data = pd.read_csv(file_path + 'Taskmaster_IMDB_Ratings.csv')

print(imdb_data.head())


heatmap_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating")
heatmap_data = heatmap_data.sort_index(ascending=False)

fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.05, right = 0.95)
sns.heatmap(
    heatmap_data,
    cmap= "RdYlGn",
    vmin=6.8, vmax=9.2,
    annot=True,
    fmt=".1f",
    linewidths=0.3,
    linecolor="darkgray",
    mask=heatmap_data.isnull(),
    cbar_kws={"label": "IMDb Rating"}
)

plt.title(f"Taskmaster IMDb Episode Ratings", fontsize=16, weight="bold")
plt.xlabel("Episode", fontsize = 14)
plt.ylabel("Season", fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.tight_layout()
plt.show()


average = round(imdb_data['Rating'].mean(),2)
print(average)
total_votes = round(imdb_data['Votes'].sum(),2)
print(total_votes)

taskmaster_overall_rating = 9.0
taskmaster_overall_votes = 31000

series_avg = []
for series in range(1, 21):

    rating_average = round(imdb_data[imdb_data['Series'] == series]['Rating'].mean(), 2)
    sum_votes = round(imdb_data[imdb_data['Series'] == series]['Votes'].sum(), 2)
    average_votes = round(imdb_data[imdb_data['Series'] == series]['Votes'].mean(), 2)
    average_rating_score = rating_average * average_votes
    
    series_avg.append([series, rating_average, sum_votes, average_votes, average_rating_score])


avg_rating_series = pd.DataFrame(series_avg, columns = ['Series', 'Rating Average', 'Sum Votes', 
                                                        'Average Votes', 'Average Rating Score'])

print(avg_rating_series)

print(avg_rating_series.sort_values(by = 'Rating Average', ascending=False).reset_index)
print(avg_rating_series.sort_values(by = 'Average Rating Score', ascending=False).reset_index)

imdb_data['Rating Score'] = imdb_data['Rating'] * imdb_data['Votes']

print(imdb_data.head())

heatmap_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating Score")
heatmap_data = heatmap_data.sort_index(ascending=False)

fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.05, right = 0.95)
sns.heatmap(
    heatmap_data,
    cmap= "RdYlGn",
    vmin=imdb_data['Rating Score'].min(), vmax=imdb_data['Rating Score'].max(),
    annot=True,
    fmt=".1f",
    linewidths=0.3,
    linecolor="darkgray",
    mask=heatmap_data.isnull(),
    cbar_kws={"label": "IMDb Score Rating"}
)

plt.title(f"Taskmaster IMDb Episode Ratings Score", fontsize=16, weight="bold")
plt.xlabel("Episode", fontsize = 14)
plt.ylabel("Season", fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.tight_layout()
plt.show()
