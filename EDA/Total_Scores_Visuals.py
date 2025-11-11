import Total_Scores_EDA as TSE
import Visual_Functions as VF

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

colours2 = colours + colours #Some plots require more than 10 bars, therefore colours are repeated for ease.

## other settings, e.g.
plt.rcParams['figure.figsize'] = (13, 7)

#Bar chart to show Number of times each seat won or lost over all series of Taskmaster
VF.bar_number_seat_wins_loses(seat_number_winner = TSE.seat_winners['Seat Number'],
                           seat_number_losers = TSE.seat_losers['Seat Number'], 
                           count_winners = TSE.seat_winners['Count Winners'], 
                           count_losers = TSE.seat_losers['Count Losers'])

# Bar charts to show Total scores summed for all series, and the averages per number of episodes
# and number of tasks
VF.summed_total_scores(dataframe = TSE.total_scores_all_series)

#Line Graph to show how the total and average (per episodes or per tasks) scores 
# for each seat changed over each series - single plot format
VF.scores_over_series_single(total_series_table = TSE.Total_per_series, 
                               total_episodes_table = TSE.Total_per_episode, 
                               total_tasks_table = TSE.Total_per_task)

#Line Graph to show how the total and average (per episodes or per tasks) scores 
# for each seat changed over each series - each seat is in its own panel
VF.scores_over_series_panelled(total_series_table = TSE.Total_per_series, 
                               total_episodes_table = TSE.Total_per_episode, 
                               total_tasks_table = TSE.Total_per_task, colour_list = colours)

#Comparing total and average (per episodes or per tasks) scores on the same plots - each 
# seat is in its own panel
VF.compare_total_avg_scores(total_series_table = TSE.Total_per_series, 
                               total_episodes_table = TSE.Total_per_episode, 
                               total_tasks_table = TSE.Total_per_task, colour_list = colours)

# Highest scores for each seat, including averages (per episodes or per tasks)
VF.highest_scores_each_seat(highest_seat_series_table = TSE.total_highest_seat,
                            highest_seat_episodes_table = TSE.episodes_highest_seat,
                            highest_seat_tasks_table = TSE.tasks_highest_seat, 
                            colour_list = colours)

# Lowest scores for each seat, including averages (per episodes or per tasks)   
VF.lowest_scores_each_seat(lowest_seat_series_table = TSE.total_lowest_seat,
                            lowest_seat_episodes_table = TSE.episodes_lowest_seat,
                            lowest_seat_tasks_table = TSE.tasks_lowest_seat, 
                            colour_list = colours)

# Final contestest positions for each series - ordered based on score
VF.final_score_seat_positions(first_table = TSE.winners_ordered, second_table = TSE.second_ordered, 
                              third_table = TSE.third_ordered, fourth_table = TSE.fourth_ordered, 
                              fifth_table = TSE.losers_ordered, colour_list = colours2,
                              top = True, top_n = 20,
                              bottom = False, bottom_n = 1)

# Final contestest positions for each series - ordered based on series
VF.final_score_seat_positions(first_table = TSE.winners_unordered, second_table = TSE.second_unordered, 
                              third_table = TSE.third_unordered, fourth_table = TSE.fourth_unordered, 
                              fifth_table = TSE.losers_unordered, colour_list = colours2,
                              top = True, top_n = 20,
                              bottom = False, bottom_n = 1)

#Final contestent positions for each series - ordered based on average score per number of episodes

VF.final_average_score_seat_positions(first_table = TSE.winners_ordered_eps, second_table = TSE.second_ordered_eps, 
                                      third_table = TSE.third_ordered_eps, fourth_table = TSE.fourth_ordered_eps, 
                               fifth_table = TSE.losers_ordered_eps, colour_list = colours2, 
                               average_type = 'episode', top = True, top_n = 20, bottom = False, 
                               bottom_n = 1)

#Final contestent positions for each series - ordered based on average score per number of tasks

VF.final_average_score_seat_positions(first_table = TSE.winners_ordered_tasks, second_table = TSE.second_ordered_tasks, 
                                      third_table = TSE.third_ordered_tasks, fourth_table = TSE.fourth_ordered_tasks, 
                               fifth_table = TSE.losers_ordered_tasks, colour_list = colours2, 
                               average_type = 'task', top = True, top_n = 20, bottom = False, 
                               bottom_n = 1)