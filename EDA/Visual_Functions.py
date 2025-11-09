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

def scores_over_series_single(total_series_table, total_episodes_table, total_tasks_table):

    for i, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        for seat in tables.columns[:5]:
            plt.plot(tables['Series'], tables[seat], 'o-', 
                lw = 3, label = f'{seat}')
        
        plt.xlabel('Series', fontsize = 20)
        plt.ylabel('Score', fontsize = 20)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.grid()
        plt.legend(loc = 'best', fontsize = 15)
        
        if i == 0:
            plt.title('The total scores for each seat over all 20 series', fontsize = 20)
        elif i == 1:
            plt.title('The total scores per number of episodes for each seat over all 20 series', fontsize = 20)
        else:
            plt.title('The total scores per number of tasks for each seat over all 20 series', fontsize = 20)

        plt.show()

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

            # ax.legend(loc = 'best', fontsize = 15, frameon=False)

        fig.supxlabel('Series', fontsize = 25)
        fig.delaxes(axes[1, 2])
        fig.legend(loc=(0.7, 0.14), fontsize = 15, frameon=False, ncol=1)

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

def compare_total_avg_scores(total_series_table, total_episodes_table, total_tasks_table, colour_list):

    fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.93, left = 0.08)

    for ax, seat, colour in zip(axes.flatten(), total_series_table.columns[:5], colour_list[:5]):

        ax.plot(total_series_table['Series'], total_series_table[seat]/4, 'o-.', 
                lw = 3, color = colour)
        
        ax.plot(total_episodes_table['Series'], total_episodes_table[seat], 'o-', 
                lw = 3, color = colour)

        ax.plot(total_tasks_table['Series'], total_tasks_table[seat]*2, 'o--', 
                lw = 3, color = colour)

        ax.plot([], [], 'o-', label = f'{seat}', color = colour, lw = 3)
        ax.set_xticks([]) 
        ax.set_yticks([])

    plt.plot([],[], 'o-.', label = 'Total Scores', lw = 3)
    plt.plot([],[], 'o-', label = 'Scores per Episodes', lw = 3)
    plt.plot([],[], 'o--', label = 'Scores per Tasks', lw = 3)
        
    fig.legend(loc=(0.7, 0.14), fontsize = 15, frameon=False, ncol=1)

    fig.supxlabel('Series', fontsize = 25)
    fig.supylabel('Average scores per tasks', fontsize = 25)

    plt.suptitle('The total scores and averages for each seat over all 20 series', fontsize = 20)
    fig.delaxes(axes[1, 2])
    plt.show()


#Highest scores for each seat and the winning contestent

def highest_scores_each_seat(total_series_table, total_episodes_table, total_tasks_table, colour_list):

    for t, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

        for i, score, name, series, seat, colour in zip(range(1, 6), tables['Max Score'],
                                        tables['Name'], tables['Series'],
                                        tables['Seat Number'], colour_list[:5]):
            plt.barh(y = name, width = score, color = colour, edgecolor = 'black')

            if t == 0:     
                plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(130, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(10, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
            elif t == 1:
                plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(12.5, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(2.5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
            else:
                plt.text(score + 0.05, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(2, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(0.5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')

        if t == 0:
            plt.xlabel('Total Score', fontsize = 18)
            plt.title('Seat Highest Scores and the Contestent Names', fontsize = 20)
        elif t == 1:    
            plt.xlabel('Average Score per Number of Episodes', fontsize = 18)
            plt.title('Seat Highest Scores per Number of Episodes and the Contestent Names', fontsize = 20)
            plt.xlim(0, 22)
        else:
            plt.xlabel('Average Score per Number of Tasks', fontsize = 18)
            plt.title('Seat Highest Scores per Number of Tasks and the Contestent Names', fontsize = 20)
            plt.xlim(0, 3.7)

        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.show()

#Lowest scores for each seat and the winning contestent

def lowest_scores_each_seat(total_series_table, total_episodes_table, total_tasks_table, colour_list):

    for t, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

        for i, score, name, series, seat, colour in zip(range(1, 6), tables['Min Score'],
                                        tables['Name'], tables['Series'],
                                        tables['Seat Number'], colour_list[:5]):
            plt.barh(y = name, width = score, color = colour, edgecolor = 'black')

            if t == 0:            
                plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(45, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(5, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
            elif t == 1:
                plt.text(score + 0.5, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(8, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(2, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
            else:
                plt.text(score + 0.05, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(1.25, i-1, str(seat), va = 'center', fontsize = 15, color = 'white')
                plt.text(0.25, i-1, str(series), va = 'center', fontsize = 15, color = 'white')
                
        if t == 0:
            plt.xlabel('Total Score', fontsize = 18)
            plt.title('Seat Lowest Scores and the Contestent Names', fontsize = 20)
        elif t == 1:
            plt.xlabel('Average Score per Number of Episodes', fontsize = 18)
            plt.title('Seat Loest Scores per Number of Episodes and the Contestent Names', fontsize = 20)
            plt.xlim(0, 15)
        else:
            plt.xlabel('Average Score per Number of Tasks', fontsize = 18)
            plt.title('Seat Lowest Scores per Number of Tasks and the Contestent Names', fontsize = 20)
            plt.xlim(0, 2.3)

        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)

        plt.show()


def final_score_seat_positions(first_table, second_table, third_table, fourth_table, fifth_table, colour_list):

    for t, tables in enumerate([first_table, second_table, third_table, fourth_table, fifth_table]):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

        for i, score, name, series, colour in zip(range(1, 21), tables['Score'],
                                        tables['Name'], 
                                        tables['Series'],  colour_list):
            plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
            plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
            plt.text(5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
        
        if t == 0:
            plt.xlim(0, 205)
            plt.title('Final Scores of First Place per Series', fontsize = 20)        
        elif t == 1:
            plt.xlim(0, 190)
            plt.title('Final Scores of Second Place per Series', fontsize = 20)
        elif t == 2:
            plt.xlim(0, 180)
            plt.title('Final Scores of Third Place per Series', fontsize = 20)
        elif t == 3:
            plt.xlim(0, 175)
            plt.title('Final Scores of Fourth Place per Series', fontsize = 20)
        else:
            plt.xlim(0, 162)
            plt.title('Final Scores of Last Place per Series', fontsize = 20)

        plt.xlabel('Total Score', fontsize = 18)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)

        plt.show()
