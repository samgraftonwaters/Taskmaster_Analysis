import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Function_Scripts import IMDB_functions as IF

import sys
sys.path.append('/Users/SamWaters/Documents/Data Science/Taskmaster/')
from Correlations import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

imdb_data = pd.read_csv(file_path + 'Taskmaster_IMDB_Ratings.csv')

print(imdb_data.head())


rating_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating")
rating_data = rating_data.sort_index(ascending=False)

print(rating_data)

IF.plot_heatmap(data = rating_data, x_label = 'Episodes', y_label = 'Series', 
                title = "Taskmaster IMDB Episode Ratings", min_range = 6.8, max_range = 9.2,
                colourbar_label = "IMDB Rating")


rating_average = round(imdb_data['Rating'].mean(),2)
print(rating_average)
total_votes = round(imdb_data['Votes'].sum(),2)
print(total_votes)

taskmaster_overall_rating = 9.0
taskmaster_overall_votes = 31000

imdb_data['Rating Score'] = imdb_data['Rating'] * imdb_data['Votes']
imdb_data['Rating Ratio'] = imdb_data['Rating'] / imdb_data['Votes']

print(imdb_data.head(10))

rating_score_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating Score")
rating_score_data  = rating_score_data .sort_index(ascending=False)

IF.plot_heatmap(data = rating_score_data , x_label = 'Episodes', y_label = 'Series', 
                title = "Taskmaster IMDB Episode Ratings Score", 
                min_range = imdb_data['Rating Score'].min(),
                max_range = imdb_data['Rating Score'].max(),
                colourbar_label = "IMDB Rating Score")
  

rating_ratio_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating Ratio")
rating_ratio_data = rating_ratio_data.sort_index(ascending=False)

IF.plot_heatmap(data = rating_ratio_data, x_label = 'Episodes', y_label = 'Series', 
                title = "Taskmaster IMDB Episode Ratings Ratio", 
                min_range = imdb_data['Rating Ratio'].min(),
                max_range = imdb_data['Rating Ratio'].max(),
                colourbar_label = "IMDB Rating Ratio", decimal_places = 3)

###Averages per series:

series_avg = []
for series in range(1, 21):

    rating_average = round(imdb_data[imdb_data['Series'] == series]['Rating'].mean(), 2)
    sum_votes = round(imdb_data[imdb_data['Series'] == series]['Votes'].sum(), 2)
    average_votes = round(imdb_data[imdb_data['Series'] == series]['Votes'].mean(), 2)
    average_rating_score =  (imdb_data[imdb_data['Series'] == series]['Rating'] * imdb_data[imdb_data['Series'] == series]['Votes']).mean()
    average_rating_ratio = (imdb_data[imdb_data['Series'] == series]['Rating'] / imdb_data[imdb_data['Series'] == series]['Votes']).mean()
    
    series_avg.append([series, rating_average, sum_votes, average_votes, 
                       average_rating_score, average_rating_ratio])


avg_rating_series = pd.DataFrame(series_avg, columns = ['Series', 'Rating Average', 'Sum Votes', 
                                                        'Average Votes', 'Average Rating Score',
                                                        'Average Rating Ratio'])

print(avg_rating_series)

print(avg_rating_series.sort_values(by = 'Rating Average', ascending=False).reset_index)
print(avg_rating_series.sort_values(by = 'Average Rating Score', ascending=False).reset_index)

IF.plot_linegraph_or_barchart(x_data = avg_rating_series['Series'], y_data = avg_rating_series['Rating Average'],
               line_colour = 'dodgerblue', x_label = 'Series', y_label = 'Average Rating', 
               title = 'Average IMDB ratings per Series', bar_or_line='line')

IF.plot_linegraph_or_barchart(x_data = avg_rating_series['Series'], y_data = avg_rating_series['Sum Votes'],
               line_colour = 'blueviolet', x_label = 'Series', y_label = 'Sum of Series Votes', 
               title = 'Sum of Votes per Series', bar_or_line='bar')

IF.plot_linegraph_or_barchart(x_data = avg_rating_series['Series'], y_data = avg_rating_series['Average Votes'],
               line_colour = 'darkorange', x_label = 'Series', y_label = 'Average Votes', 
               title = 'Average Votes per Series', bar_or_line='bar')

IF.plot_linegraph_or_barchart(x_data = avg_rating_series['Series'], y_data = avg_rating_series['Average Rating Score'],
               line_colour = 'magenta', x_label = 'Series', y_label = 'Average Rating Score', 
               title = 'Average Rating Score per Series', bar_or_line='bar')


episodes_per_series = imdb_data.groupby('Series')['Episode'].count().tolist()

midpoints = []
start = 1

for n in episodes_per_series:
    midpoint = start + (n - 1) / 2
    midpoints.append(midpoint)
    start += n

series_boundaries = []
running = 1

for val in episodes_per_series:
    running += val
    series_boundaries.append(running)

IF.line_plot_episodes_series(episode_x = imdb_data['Episode'], episode_y = imdb_data['Rating'], 
                          series_x = midpoints, series_y = avg_rating_series['Rating Average'], 
                          series_boundaries = series_boundaries, series_number_col = avg_rating_series['Series'],
                          x_label = 'Episodes', y_label = 'IMDB Ratings',
                          title = 'IMDB Rating per Episode and Averaged over each Series')

IF.line_plot_episodes_series(episode_x = imdb_data['Episode'], episode_y = imdb_data['Votes'], 
                          series_x = midpoints, series_y = avg_rating_series['Average Votes'], 
                          series_boundaries = series_boundaries, series_number_col = avg_rating_series['Series'],
                          x_label = 'Episodes', y_label = 'Number of Votes',
                          title = 'Number of Rating Votes per Episode and Averaged over each Series')

IF.line_plot_episodes_series(episode_x = imdb_data['Episode'], episode_y = imdb_data['Rating Score'], 
                          series_x = midpoints, series_y = avg_rating_series['Average Rating Score'], 
                          series_boundaries = series_boundaries, series_number_col = avg_rating_series['Series'],
                          x_label = 'Episodes', y_label = 'Rating Score',
                          title = 'Rating Score per Episode and Averaged over each Series')

IF.line_plot_episodes_series(episode_x = imdb_data['Episode'], episode_y = imdb_data['Rating Ratio'], 
                          series_x = midpoints, series_y = avg_rating_series['Average Rating Ratio'], 
                          series_boundaries = series_boundaries, series_number_col = avg_rating_series['Series'],
                          x_label = 'Episodes', y_label = 'Rating Ratio',
                          title = 'Rating Ratio per Episode and Averaged over each Series')

## correlation between number of votes and ratings and each series?

print(imdb_data.corr())

correlations = imdb_data.corr(method = 'spearman')

grouped_variables = CF.group_corr_variables(correlations)
high_corr = CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.8).reset_index(drop = True)

print(high_corr)

high_corr, cmap, norm = CF.set_correlation_colours(data_table = high_corr, corr_column = 'correlation', limits = 1)

fig, axes = plt.subplots(nrows = 3, ncols = 2)
plt.subplots_adjust(wspace=0.1, hspace=0.1, bottom = 0.08, top = 0.98, left = 0.05, right = 0.95)

for row, ax in enumerate(axes.flatten()[:len(high_corr)]):

    ax.scatter(imdb_data[high_corr['var_1'][row]], imdb_data[high_corr['var_2'][row]], 
            color = high_corr['colour'][row]) 
    ax.plot([], [], color = 'white', label = f"{round(high_corr['correlation'][row],2)}")
    ax.set_xlabel(high_corr['var_1'][row])
    ax.set_ylabel(high_corr['var_2'][row])
    legend = ax.legend(frameon=True, loc = 'best', labelcolor = 'white', 
                    facecolor = high_corr['colour'][row])
plt.show()

min_max_ratings = []
for series in range(1, 21):

    series_df = imdb_data[imdb_data['Series'] == series]

    min_rating = series_df['Rating'].min()
    max_rating = series_df['Rating'].max()

    min_episode = series_df[series_df['Rating'] == min_rating]['Episode'].values
    max_episode = series_df[series_df['Rating'] == max_rating]['Episode'].values

    min_max_ratings.append({
        'Series': series,
        'Min_Rating': min_rating,
        'Min_Episodes': min_episode,
        'Max_Rating': max_rating,
        'Max_Episodes': max_episode
    })

print(pd.DataFrame(min_max_ratings))