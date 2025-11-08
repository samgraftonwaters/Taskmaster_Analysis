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

VF.bar_number_seat_wins_loses(seat_number_winner = TSE.seat_winners['Seat Number'],
                           seat_number_losers = TSE.seat_losers['Seat Number'], 
                           count_winners = TSE.seat_winners['Count Winners'], 
                           count_losers = TSE.seat_losers['Count Losers'])

# plt.bar(x = TSE.seat_winners['Seat Number']-0.2, height = TSE.seat_winners['Count Winners'], 
#         label = 'Number of Wins', width = 0.40, color = 'blue', alpha = 0.6, edgecolor ='black')
# plt.bar(x = TSE.seat_losers['Seat Number']+0.2, height = TSE.seat_losers['Count Losers'], 
#         label = 'Number of Loses', width = 0.40, color = 'green', alpha = 0.6, edgecolor ='black')

# for i in range(5):
#     plt.text(i+0.8, TSE.seat_winners['Count Winners'][i]+0.05, 
#              TSE.seat_winners['Count Winners'][i], ha='center', fontsize = 15, color = 'blue')
#     plt.text(i+1.2, TSE.seat_losers['Count Losers'][i]+0.05, 
#              TSE.seat_losers['Count Losers'][i], ha='center', fontsize = 15, color = 'green')

# plt.title('The number of wins or loses per seat in all 20 Series of Taskmaster', fontsize = 16)
# plt.xlabel('Seat Number', fontsize = 14)
# plt.ylabel('Count', fontsize = 14)
# plt.xticks(fontsize = 12)
# plt.yticks(fontsize = 12)
# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# ##Total scores and averages for all series summed/combined

# #Total

# plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[0]].values[0][0:5], 
#         label = 'Number of Wins', width = 0.5, color = 'blue', alpha = 0.6, edgecolor ='black')

# for i in range(5):
#     plt.text(i+1, TSE.total_scores_all_series.iloc[[0]].values[0][0:5][i]+0.5, 
#              TSE.total_scores_all_series.iloc[[0]].values[0][0:5][i], ha='center', fontsize = 15, color = 'blue')

# plt.hlines(TSE.total_scores_all_series.iloc[[0]].values[0][6], 0, 6, lw = 5, linestyle = '--',
#            label = f'Average = {TSE.total_scores_all_series.iloc[[0]].values[0][6]}', color = 'purple')

# plt.title('The Total Score per seat in all 20 Series of Taskmaster', fontsize = 16)
# plt.ylim(2700, 2820)
# plt.xlim(0.5, 5.5)
# plt.xlabel('Seat Number', fontsize = 14)
# plt.ylabel('Total Score', fontsize = 14)
# plt.xticks(fontsize = 12)
# plt.yticks(fontsize = 12)
# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# #Per number of Episodes

# plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[1]].values[0][0:5], 
#         label = 'Number of Wins', width = 0.5, color = 'green', alpha = 0.6, edgecolor ='black')

# for i in range(5):
#     plt.text(i+1, TSE.total_scores_all_series.iloc[[1]].values[0][0:5][i]+0.1, 
#              TSE.total_scores_all_series.iloc[[1]].values[0][0:5][i], ha='center', fontsize = 15, 
#              color = 'green')

# plt.hlines(TSE.total_scores_all_series.iloc[[1]].values[0][6], 0, 6, lw = 5, linestyle = '--',
#            label = f'Average = {TSE.total_scores_all_series.iloc[[1]].values[0][6]}', color = 'red')

# plt.title('The Total Score per Number of Episodes for each seat in all 20 Series of Taskmaster', fontsize = 16)
# plt.ylim(14, 16)
# plt.xlim(0.5, 5.5)
# plt.xlabel('Seat Number', fontsize = 14)
# plt.ylabel('Total Score per Number of Episodes', fontsize = 14)
# plt.xticks(fontsize = 12)
# plt.yticks(fontsize = 12)
# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# #Per number of Tasks
# plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[2]].values[0][0:5], 
#         label = 'Number of Wins', width = 0.5, color = 'orange', alpha = 0.6, edgecolor ='black')

# for i in range(5):
#     plt.text(i+1, TSE.total_scores_all_series.iloc[[2]].values[0][0:5][i]+0.012, 
#              TSE.total_scores_all_series.iloc[[2]].values[0][0:5][i], ha='center', fontsize = 15, 
#              color = 'darkorange')

# plt.hlines(TSE.total_scores_all_series.iloc[[2]].values[0][6], 0, 6, lw = 5, linestyle = '--',
#            label = f'Average = {TSE.total_scores_all_series.iloc[[2]].values[0][6]}', color = 'blue')

# plt.title('The Total Score per Number of Tasks for each seat in all 20 Series of Taskmaster', fontsize = 16)
# plt.ylim(2.5, 2.7)
# plt.xlim(0.5, 5.5)
# plt.xlabel('Seat Number', fontsize = 14)
# plt.ylabel('Total Score per Number of Tasks', fontsize = 14)
# plt.xticks(fontsize = 12)
# plt.yticks(fontsize = 12)
# plt.legend(loc = 'best', fontsize = 15)
# plt.show()


# #Total scores per seat for each series

# for seat in TSE.Total_per_series.columns[:5]:
#     plt.plot(TSE.Total_per_series['Series'], TSE.Total_per_series[seat], 'o-', 
#              lw = 3, label = f'{seat}')
    
# plt.xlabel('Series', fontsize = 20)
# plt.ylabel('Score', fontsize = 20)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid()
# plt.title('The total scores for each seat over all 20 series', fontsize = 20)

# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
# plt.subplots_adjust(wspace=0, hspace=0)
# for ax, seat, colour in zip(axes.flatten(), TSE.Total_per_series.columns[:5], colours[:5]):

#     ax.plot(TSE.Total_per_series['Series'], TSE.Total_per_series[seat], 'o-', 
#              lw = 3, label = f'{seat}', color = colour)

#     ax.tick_params(axis='x', labelsize=12)
#     ax.tick_params(axis='y', labelsize=15)

#     ticks = ax.get_xticks()              
#     ax.set_xticks(ticks[::2])   

#     ax.legend(loc = 'best', fontsize = 15, frameon=False)

# fig.supxlabel('Series', fontsize = 25)
# fig.supylabel('Scores', fontsize = 25)

# plt.suptitle('The total scores for each seat over all 20 series', fontsize = 20)
# fig.delaxes(axes[1, 2])
# plt.show()



# #Total scores per number of episodes in each seat for each series

# for seat in TSE.Total_per_episode.columns[:5]:
#     plt.plot(TSE.Total_per_episode['Series'], TSE.Total_per_episode[seat], 'o-', 
#              lw = 3, label = f'{seat}')
    
# plt.xlabel('Series', fontsize = 20)
# plt.ylabel('Average score per Episode', fontsize = 20)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid()
# plt.title('The total scores per number of episodes for each seat over all 20 series', fontsize = 20)

# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
# plt.subplots_adjust(wspace=0, hspace=0)
# for ax, seat, colour in zip(axes.flatten(), TSE.Total_per_episode.columns[:5], colours[:5]):

#     ax.plot(TSE.Total_per_episode['Series'], TSE.Total_per_episode[seat], 'o-', 
#              lw = 3, label = f'{seat}', color = colour)

#     ax.tick_params(axis='x', labelsize=12)
#     ax.tick_params(axis='y', labelsize=15)

#     ticks = ax.get_xticks()              
#     ax.set_xticks(ticks[::2])   
    
#     ax.legend(loc = 'best', fontsize = 15, frameon=False)

# fig.supxlabel('Series', fontsize = 25)
# fig.supylabel('Average scores per episode', fontsize = 25)

# plt.suptitle('The total scores per number of episode for each seat over all 20 series', fontsize = 20)
# fig.delaxes(axes[1, 2])
# plt.show()

# #Total scores per number of tasks in each seat for each series

# for seat in TSE.Total_per_task.columns[:5]:
#     plt.plot(TSE.Total_per_task['Series'], TSE.Total_per_task[seat], 'o-', 
#              lw = 3, label = f'{seat}')
    
# plt.xlabel('Series', fontsize = 20)
# plt.ylabel('Average scores per tasks', fontsize = 20)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid()
# plt.title('The total scores per number of tasks for each seat over all 20 series', fontsize = 20)

# plt.legend(loc = 'best', fontsize = 15)
# plt.show()

# fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
# plt.subplots_adjust(wspace=0, hspace=0)
# for ax, seat, colour in zip(axes.flatten(), TSE.Total_per_task.columns[:5], colours[:5]):

#     ax.plot(TSE.Total_per_task['Series'], TSE.Total_per_task[seat], 'o-', 
#              lw = 3, label = f'{seat}', color = colour)

#     ax.tick_params(axis='x', labelsize=12)
#     ax.tick_params(axis='y', labelsize=15)

#     ticks = ax.get_xticks()              
#     ax.set_xticks(ticks[::2])   
    
#     ax.legend(loc = 'best', fontsize = 15, frameon=False)

# fig.supxlabel('Series', fontsize = 25)
# fig.supylabel('Average scores per tasks', fontsize = 25)

# plt.suptitle('The total scores per number of tasks for each seat over all 20 series', fontsize = 20)
# fig.delaxes(axes[1, 2])
# plt.show()


# ### Total scores, and averages per episodes and tasks

# fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.93, left = 0.08)

# for ax, seat, colour in zip(axes.flatten(), TSE.Total_per_task.columns[:5], colours[:5]):

#     ax.plot(TSE.Total_per_series['Series'], TSE.Total_per_series[seat]/4, 'o-.', 
#              lw = 3, color = colour)
    
#     ax.plot(TSE.Total_per_episode['Series'], TSE.Total_per_episode[seat], 'o-', 
#             lw = 3, color = colour)

#     ax.plot(TSE.Total_per_task['Series'], TSE.Total_per_task[seat]*2, 'o--', 
#              lw = 3, color = colour)

#     ax.plot([], [], 'o-', label = f'{seat}', color = colour, lw = 3)
#     ax.set_xticks([]) 
#     ax.set_yticks([])

# plt.plot([],[], 'o-.', label = 'Total Scores', lw = 3)
# plt.plot([],[], 'o-', label = 'Scores per Episodes', lw = 3)
# plt.plot([],[], 'o--', label = 'Scores per Tasks', lw = 3)
    
# fig.legend(loc=(0.7, 0.14), fontsize = 15, frameon=False, ncol=1)

# fig.supxlabel('Series', fontsize = 25)
# fig.supylabel('Average scores per tasks', fontsize = 25)

# plt.suptitle('The total scores and averages for each seat over all 20 series', fontsize = 20)
# fig.delaxes(axes[1, 2])
# plt.show()


#Highest scores for each seat and the winning contestent

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.total_highest_seat['Max Score'],
#                                   TSE.total_highest_seat['Name'], TSE.total_highest_seat['Series'],
#                                   TSE.total_highest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(130, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(10, i-1, str(series), va = 'center', fontsize = 15, color = 'white')

# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Highest Scores and the Contestent Names', fontsize = 20)
# plt.show()

# #Lowest scores for each seat and the winning contestent

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.total_lowest_seat['Min Score'],
#                                   TSE.total_lowest_seat['Name'], TSE.total_lowest_seat['Series'],
#                                   TSE.total_lowest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(45, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')

# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Lowest Scores and the Contestent Names', fontsize = 20)
# plt.show()

# #Highest scores for each seat and the winning contestent - average per number of episodes

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.episodes_highest_seat['Max Score'],
#                                   TSE.episodes_highest_seat['Name'], TSE.episodes_highest_seat['Series'],
#                                   TSE.episodes_highest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(12.5, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(2.5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
# plt.xlim(0, 22)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Highest Scores per Number of Episodes and the Contestent Names', fontsize = 20)
# plt.show()

# #Lowest scores for each seat and the winning contestent - average per number of episodes

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.episodes_lowest_seat['Min Score'],
#                                   TSE.episodes_lowest_seat['Name'], TSE.episodes_lowest_seat['Series'],
#                                   TSE.episodes_lowest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(8, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(2, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
# plt.xlim(0, 15)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Lowest Scores per Number of Episodes and the Contestent Names', fontsize = 20)
# plt.show()


# #Highest scores for each seat and the winning contestent - average per number of tasks

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.tasks_highest_seat['Max Score'],
#                                   TSE.tasks_highest_seat['Name'], TSE.tasks_highest_seat['Series'],
#                                   TSE.tasks_highest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.05, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(2, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(0.5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
# plt.xlim(0, 3.7)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Highest Scores per Number of Tasks and the Contestent Names', fontsize = 20)
# plt.show()

# #Lowest scores for each seat and the winning contestent - average per number of tasks

# fig, axes = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

# for i, score, name, series, seat, colour in zip(range(1, 6), TSE.tasks_lowest_seat['Min Score'],
#                                   TSE.tasks_lowest_seat['Name'], TSE.tasks_lowest_seat['Series'],
#                                   TSE.tasks_lowest_seat['Seat Number'], colours[:5]):
#     plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
#     plt.text(score + 0.05, i-1, str(score), va='center', fontsize = 15, color = colour)  
#     plt.text(1.25, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
#     plt.text(0.25, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
# plt.xlim(0, 2.3)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.xlabel('Total Score', fontsize = 18)
# plt.title('Seat Lowest Scores per Number of Tasks and the Contestent Names', fontsize = 20)
# plt.show()

fig, axes = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

for i, score, name, series, colour in zip(range(1, 21), TSE.winners['Score'],
                                  TSE.winners['Name'], 
                                  TSE.winners['Series'],  colours2):
    plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
    plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
    plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
plt.xlim(0, 200)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Total Score', fontsize = 18)
plt.title('Final Scores of First Place per Series', fontsize = 20)
plt.show()


fig, axes = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

for i, score, name, series, colour in zip(range(1, 21), TSE.second['Score'],
                                  TSE.second['Name'], 
                                  TSE.second['Series'],  colours2):
    plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
    plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
    plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
plt.xlim(0, 190)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Total Score', fontsize = 18)
plt.title('Final Scores of Second Place per Series', fontsize = 20)
plt.show()


fig, axes = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

for i, score, name, series, colour in zip(range(1, 21), TSE.third['Score'],
                                  TSE.third['Name'], 
                                  TSE.third['Series'],  colours2):
    plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
    plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
    plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
plt.xlim(0, 180)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Total Score', fontsize = 18)
plt.title('Final Scores of Third Place per Series', fontsize = 20)
plt.show()

fig, axes = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

for i, score, name, series, colour in zip(range(1, 21), TSE.fourth['Score'],
                                  TSE.fourth['Name'], 
                                  TSE.fourth['Series'],  colours2):
    plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
    plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
    plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
plt.xlim(0, 175)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Total Score', fontsize = 18)
plt.title('Final Scores of Fourth Place per Series', fontsize = 20)
plt.show()


fig, axes = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

for i, score, name, series, colour in zip(range(1, 21), TSE.losers['Score'],
                                  TSE.losers['Name'], 
                                  TSE.losers['Series'],  colours2):
    plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
    plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
    plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
plt.xlim(0, 162)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Total Score', fontsize = 18)
plt.title('Final Scores of Last Place per Series', fontsize = 20)
plt.show()