import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def bar_number_seat_wins_loses(seat_number_winner, seat_number_losers, count_winners, count_losers):

    """
    Plot to show the number of times each seat won a series or lost a series. One of figure so all
    figure annotations are kept in. Only the x and y values (columns from dataframes) are called in.

    Parameters:
    -----------
        seat_number_winner (dataframe column): column that contains the seat number from winners table
        seat_number_losers (dataframe column): column that contains the seat number from losers table
        count_winners (dataframe column): column of count each seat won
        count_losers (dataframe column): column of count each seat lost

    Returns:
    --------
        Bar chart with number of times each seat won or lost for all 20 series of Taskmaster
    
    """

    fig, axes = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.15)

    plt.bar(x = seat_number_winner-0.2, height = count_winners, 
            label = 'Number of Wins', width = 0.40, color = 'blue', alpha = 0.6, edgecolor ='black')
    plt.bar(x = seat_number_losers+0.2, height = count_losers, 
            label = 'Number of Loses', width = 0.40, color = 'green', alpha = 0.6, edgecolor ='black')

    for i in range(5):
        plt.text(i+0.8, count_winners[i]+0.05, 
                count_winners[i], ha='center', fontsize = 15, color = 'blue')
        plt.text(i+1.2, count_losers[i]+0.05, 
                count_losers[i], ha='center', fontsize = 15, color = 'green')

    plt.title('The number of wins or loses per seat in all 20 Series of Taskmaster', fontsize = 16)
    plt.xlabel('Seat Number', fontsize = 14)
    plt.ylabel('Count', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(loc = 'best', fontsize = 15)
    plt.show()


# ##Total scores and averages for all series summed/combined

def summed_total_scores(dataframe):

    for score, bar_colour, mean_colour in zip(range(3), ['blue', 'green', 'darkorange'], ['orange', 'red', 'blue']):

        plt.bar(x = range(1,6), height = dataframe.iloc[[score]].values[0][0:5], 
           label = 'Number of Wins', width = 0.5, color = bar_colour, alpha = 0.6, edgecolor ='black')

        plt.hlines(dataframe.iloc[[score]].values[0][6], 0, 6, lw = 5, linestyle = '--',
            label = f'Average = {dataframe.iloc[[score]].values[0][6]}', 
            color = mean_colour)
                    
        if score == 0:
            plt.title('The Total Score per seat in all 20 Series of Taskmaster', fontsize = 16)
            plt.ylim(2700, 2820)
            for i in range(5):
                plt.text(i+1, dataframe.iloc[[score]].values[0][0:5][i] + 0.5, 
                        dataframe.iloc[[score]].values[0][0:5][i], ha='center', 
                        fontsize = 15, color = bar_colour)

        elif score == 1:
            plt.title('The Total Score per Number of Episodes for each seat in all 20 Series of Taskmaster', fontsize = 16)
            plt.ylim(14, 16.2)    
            for i in range(5):
                plt.text(i+1, dataframe.iloc[[score]].values[0][0:5][i] + 0.1, 
                        dataframe.iloc[[score]].values[0][0:5][i], ha='center', 
                        fontsize = 15, color = bar_colour)

        else:
            plt.title('The Total Score per Number of Tasks for each seat in all 20 Series of Taskmaster', fontsize = 16)
            plt.ylim(2.5, 2.7)
            for i in range(5):
                plt.text(i+1, dataframe.iloc[[score]].values[0][0:5][i] + 0.01, 
                        dataframe.iloc[[score]].values[0][0:5][i], ha='center', 
                        fontsize = 15, color = bar_colour)

        plt.xlim(0.5, 5.5)
        plt.xlabel('Seat Number', fontsize = 18)
        plt.ylabel('Total Score', fontsize = 18)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.legend(loc = 'upper left', fontsize = 16)
        plt.show()


#Total scores per seat for each series

# def scores_over_series_single():

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

def scores_over_series_panelled(total_series_table, total_episodes_table, total_tasks_table, colour_list):

    for i, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
        plt.subplots_adjust(wspace=0, hspace=0)

        for ax, seat, colour in zip(axes.flatten(), tables[:5], colour_list[:5]):

            ax.plot(tables['Series'], tables[seat], 'o-', 
                lw = 3, label = f'{seat}', color = colour)

            ax.tick_params(axis='x', labelsize=12)
            ax.tick_params(axis='y', labelsize=15)

            ticks = ax.get_xticks()              
            ax.set_xticks(ticks[::2])   

            ax.legend(loc = 'best', fontsize = 15, frameon=False)

        fig.supxlabel('Series', fontsize = 25)
        fig.delaxes(axes[1, 2])

        if i == 0:
            fig.supylabel('Total Score', fontsize = 25)
            plt.suptitle('The total scores for each seat over all 20 series', fontsize = 20)
        
        elif i == 1:
            fig.supylabel('Average Scores per Episodes', fontsize = 25)
            plt.suptitle('The total scores per number of episode for each seat over all 20 series', fontsize = 20)

        else:
            fig.supylabel('Average Scores per Tasks', fontsize = 25)
            plt.suptitle('The total scores per number of tasks for each seat over all 20 series', fontsize = 20)

        plt.show()

