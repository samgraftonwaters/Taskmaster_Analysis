import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Function_Scripts import IMDB_functions as IF

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

print(imdb_data.head())

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
    average_rating_score = rating_average * average_votes
    
    series_avg.append([series, rating_average, sum_votes, average_votes, average_rating_score])


avg_rating_series = pd.DataFrame(series_avg, columns = ['Series', 'Rating Average', 'Sum Votes', 
                                                        'Average Votes', 'Average Rating Score'])

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

fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.95)
plt.plot(range(1, len(imdb_data)+1), imdb_data['Rating'], '-o', color = 'dodgerblue', lw = 3)
plt.show()
### Add line plots
#### Create function scipt for methods and plots
## correlation between number of votes and ratings and each series?
