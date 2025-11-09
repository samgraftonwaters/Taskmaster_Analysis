import Total_Scores_EDA as TSE
import Visual_Functions as VF

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

colours2 = colours + colours

#### Visual Settings
# plt.style.use('ggplot')

## other settings, e.g.
plt.rcParams['figure.figsize'] = (13, 7)


#Number of times each seat won or lost over all series of Taskmaster

# VF.bar_number_seat_wins_loses(seat_number_winner = TSE.seat_winners['Seat Number'],
#                            seat_number_losers = TSE.seat_losers['Seat Number'], 
#                            count_winners = TSE.seat_winners['Count Winners'], 
#                            count_losers = TSE.seat_losers['Count Losers'])


# VF.summed_total_scores(dataframe = TSE.total_scores_all_series)
# VF. scores_over_series_single(total_series_table = TSE.Total_per_series, 
#                                total_episodes_table = TSE.Total_per_episode, 
#                                total_tasks_table = TSE.Total_per_task)

# VF.scores_over_series_panelled(total_series_table = TSE.Total_per_series, 
#                                total_episodes_table = TSE.Total_per_episode, 
#                                total_tasks_table = TSE.Total_per_task, colour_list = colours)


# VF.compare_total_avg_scores(total_series_table = TSE.Total_per_series, 
#                                total_episodes_table = TSE.Total_per_episode, 
#                                total_tasks_table = TSE.Total_per_task, colour_list = colours)

# VF.highest_scores_each_seat(total_series_table = TSE.total_highest_seat,
#                             total_episodes_table = TSE.episodes_highest_seat,
#                             total_tasks_table = TSE.tasks_highest_seat, 
#                             colour_list = colours)
    
# VF.lowest_scores_each_seat(total_series_table = TSE.total_lowest_seat,
#                             total_episodes_table = TSE.episodes_lowest_seat,
#                             total_tasks_table = TSE.tasks_lowest_seat, 
#                             colour_list = colours)


VF.final_score_seat_positions(first_table = TSE.winners, second_table = TSE.second, 
                              third_table = TSE.third, fourth_table = TSE.fourth, 
                              fifth_table = TSE.losers, colour_list = colours2)
