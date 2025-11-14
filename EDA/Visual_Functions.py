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

    """
    Plots for the total scores summed or average scores for each seat.

    Parameters:
    -----------
        dataframe (dataframe): table that contains total scores summed for each seat and then the
        averages per number of episodes and number of tasks taken from this score.
    
    Returns:
    --------
        Three bar charts for each set of values and their means of each seat   
    
    """

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
            plt.ylim(2.5, 2.72)
            for i in range(5):
                plt.text(i+1, dataframe.iloc[[score]].values[0][0:5][i] + 0.013, 
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

    """
    Plots total scores and averages per number of episodes and tasks over the course of each series 
    for each seat.

    Parameters:
    -----------
        total_series_table (dataframe): dataframe with total scores for each series for each respective seat
        total_episodes_table (dataframe): dataframe with average total scores per number of episodes
                                        for each series for each respective seat
        total_tasks_table (dataframe): dataframe with average total scores per number of tasks
                                        for each series for each respective seat
    
    Returns:
    --------
        Three separate line or bump plots where all 5 seats are compared over all series
    
    """

    for i, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08)

        for seat in tables.columns[:5]:
            plt.plot(tables['Series'], tables[seat], 'o-', 
                lw = 3, label = f'{seat}')
        
        plt.xlabel('Series', fontsize = 20)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.grid()
        plt.legend(loc = 'best', fontsize = 15)
        
        if i == 0:
            plt.title('The total scores for each seat over all 20 series', fontsize = 20)
            plt.ylabel('Total Score', fontsize = 20)
        elif i == 1:
            plt.title('The average scores per number of episodes for each seat over all 20 series', fontsize = 20)
            plt.ylabel('Average Score per Episodes', fontsize = 20)
        else:
            plt.title('The average scores per number of tasks for each seat over all 20 series', fontsize = 20)
            plt.ylabel('Average Score per Tasks', fontsize = 20)

        plt.show()

def scores_over_series_panelled(total_series_table, total_episodes_table, total_tasks_table, colour_list):

    """
    Plots total scores and averages per number of episodes and tasks over the course of each series, where
    each seat is in it's own panel

    Parameters:
    -----------
        total_series_table (dataframe): dataframe with total scores for each series for each respective seat
        total_episodes_table (dataframe): dataframe with average total scores per number of episodes
                                        for each series for each respective seat
        total_tasks_table (dataframe): dataframe with average total scores per number of tasks
                                        for each series for each respective seat
        colour_list (list): list of colours for each panel (seats)
    
    Returns:
    --------
        Three separate line or bump plots where all 5 seats are compared over all series, presented
        in their own panels
    
    """
        
    for i, tables in enumerate([total_series_table, total_episodes_table, total_tasks_table]):

        fig, axes = plt.subplots(nrows = 2, ncols = 3, sharex = False, sharey = True)
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.1)

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

    """
    Compares total scores, averages per number of episodes and average per number of tasks 
    over the course of each series on the same figure, where each seat is in it's own panel

    Parameters:
    -----------
        total_series_table (dataframe): dataframe with total scores for each series for each respective seat
        total_episodes_table (dataframe): dataframe with average total scores per number of episodes
                                        for each series for each respective seat
        total_tasks_table (dataframe): dataframe with average total scores per number of tasks
                                        for each series for each respective seat
        colour_list (list): list of colours for each panel (seats)
    
    Returns:
    --------
        Line or bump plots comparing totals and averages per number of episodes and tasks on the same plot,
        where all 5 seats are compared over all series, presented in their own panels
    
    """

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

def highest_scores_each_seat(highest_seat_series_table, highest_seat_episodes_table, 
                             highest_seat_tasks_table, colour_list):

    """
    Highest scores for each seat only

    Parameters:
    -----------
        highest_seat_series_table (dataframe): dataframe with the highest scores for each seat seat
        highest_seat_episodes_table (dataframe): dataframe with highest average total scores per number of episodes
                                        for each seat
        highest_seat_tasks_table (dataframe): dataframe with highest average total scores per number of tasks
                                        for each seat
        colour_list (list): list of colours for each seat
    
    Returns:
    --------
        Bar charts for the highest scores and average scores for each seat only. 
    
    """

    for t, tables in enumerate([highest_seat_series_table, highest_seat_episodes_table, highest_seat_tasks_table]):

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

def lowest_scores_each_seat(lowest_seat_series_table, lowest_seat_episodes_table,
                            lowest_seat_tasks_table, colour_list):

    """
    Lowest scores for each seat only

    Parameters:
    -----------
        lowest_seat_series_table (dataframe): dataframe with the lowest scores for each seat seat
        lowest_seat_episodes_table (dataframe): dataframe with lowest average total scores per number of episodes
                                        for each seat
        lowest_seat_tasks_table (dataframe): dataframe with lowest average total scores per number of tasks
                                        for each seat
        colour_list (list): list of colours for each seat
    
    Returns:
    --------
        Bar charts for the lowest scores and average scores for each seat only. 
    
    """

    for t, tables in enumerate([lowest_seat_series_table, lowest_seat_episodes_table,
                                lowest_seat_tasks_table]):

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
            plt.title('Seat Lowest Scores per Number of Episodes and the Contestent Names', fontsize = 20)
            plt.xlim(0, 15)
        else:
            plt.xlabel('Average Score per Number of Tasks', fontsize = 18)
            plt.title('Seat Lowest Scores per Number of Tasks and the Contestent Names', fontsize = 20)
            plt.xlim(0, 2.3)

        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)

        plt.show()


def final_score_seat_positions(position_tables, colour_list, top = True, top_n = 20, bottom = False, 
                               bottom_n = 1):

    """
    Comparing the contestents who finish in their respective positions over each series based on total
    scores.

    Parameters:
    -----------
        position_table (dataframe): dataframe that contains all contestent positions and scores
        colour_list (list): list of colours for each contestent
        top (boolean): If true, the top contestestents for each possition will be displayed. Use next
                       parameter to set the number to show. Default = True
        top_n (int): Number of "top" contestents to be displayed. Default = 20
        bottom (boolean): If true, the bottom contestestents for each possition will be displayed. 
                        Use next parameter to set the number to show. Default = False
        bottom_n (int): Number of "bottom" contestents to be displayed. Default = 1
    
    Returns:
    --------
        Five different bar charts, one for each position, comparing all series contestents together,
        either showing the top or bottom number
    
    """

    for pos in range(1, 6):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

        position_data = position_tables[position_tables['Position'] == pos]

        if top == True:

            position_data = position_data[20 - top_n : 21]
            if top_n < 20:
                title = f'(Top {top_n})'
            else:
                title = ''
            
            for i, score, name, series, seat, colour in zip(range(1, 21), position_data['Score'],
                                            position_data['Name'], 
                                            position_data['Series'],
                                            position_data['Seat'], colour_list):
                plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
                plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(10, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
                plt.text(25, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')
        
        if bottom == True:
            position_data = position_data[0 : bottom_n] 
            if bottom_n < 20:
                title = f'(Bottom {bottom_n})'
            else:
                title = ''
            
            for i, score, name, series, seat, colour in zip(range(1, 21), position_data['Score'],
                                position_data['Name'], 
                                position_data['Series'],
                                position_data['Seat'], colour_list):
                plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
                plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(10, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
                plt.text(25, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')

        if pos == 1:        
            plt.xlim(0, 205)
            plt.title(f'Final Scores of First Place per Series {title}', fontsize = 20)        
        elif pos == 2:
            plt.xlim(0, 190)
            plt.title(f'Final Scores of Second Place per Series {title}', fontsize = 20)
        elif pos == 3:
            plt.xlim(0, 180)
            plt.title(f'Final Scores of Third Place per Series {title}', fontsize = 20)
        elif pos == 4:
            plt.xlim(0, 175)
            plt.title(f'Final Scores of Fourth Place per Series {title}', fontsize = 20)
        else:
            plt.xlim(0, 162)
            plt.title(f'Final Scores of Last Place per Series {title}', fontsize = 20)

        plt.xlabel('Total Score', fontsize = 18)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)

        plt.show()


def final_average_score_seat_positions(position_tables, colour_list, average_type, top = True, 
                                       top_n = 20, bottom = False, bottom_n = 1):

    """
    Comparing the contetestents who finish in their respective positions over each series based on
    their average scores per number of episodes or number of tasks.

    Parameters:
    -----------
        position_table (dataframe): dataframe that contains all contestent positions and scores
        colour_list (list): list of colours for each contestent
        average type (string): States the type of average being plotted. If average per task data is used
                        this should be set to "task"; if average per episode data is used this should be
                        set to "episode"
        top (boolean): If true, the top contestestents for each possition will be displayed. Use next
                       parameter to set the number to show. Default = True
        top_n (int): Number of "top" contestents to be displayed. Default = 20
        bottom (boolean): If true, the bottom contestestents for each possition will be displayed. 
                        Use next parameter to set the number to show. Default = False
        bottom_n (int): Number of "bottom" contestents to be displayed. Default = 1
    
    Returns:
    --------
        Five different bar charts, one for each position, comparing all series contestents together,
        either showing the top or bottom number
    
    """

    for pos in range(1, 6):

        fig, axes = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

        position_data = position_tables[position_tables['Position'] == pos]

        if top == True:

            position_data = position_data[20 - top_n : 21]
            if top_n < 20:
                title = f'(Top {top_n})'
            else:
                title = ''
            
            for i, score, name, series, seat, colour in zip(range(1, 21), position_data['Score'],
                                            position_data['Name'], 
                                            position_data['Series'],
                                            position_data['Seat'], colour_list):
                plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
                plt.text(score + 0.25, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(0.5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
                plt.text(1.7, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')
        
        if bottom == True:
            position_data = position_data[0 : bottom_n] 
            if bottom_n < 20:
                title = f'(Bottom {bottom_n})'
            else:
                title = ''
            
            for i, score, name, series, seat, colour in zip(range(1, 21), position_data['Score'],
                                position_data['Name'], 
                                position_data['Series'], 
                                 position_data['Seat'],  colour_list):
                plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
                plt.text(score + 0.25, i-1, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(0.5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
                plt.text(1.7, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')

        
        if average_type == 'task':
            plt.xlabel('Average Score per Number of Tasks', fontsize = 18)
            if pos == 1:
                plt.title(f'Average Score per Number of Tasks for First Place per Series {title}', fontsize = 20)        
                plt.xlim(0, 4)
            elif pos == 2:
                plt.title(f'Average Score per Number of Tasks for Second Place per Series {title}', fontsize = 20)
                plt.xlim(0, 3.6)
            elif pos == 3:
                plt.title(f'Average Score per Number of Tasks for Third Place per Series {title}', fontsize = 20)
                plt.xlim(0, 3.4)
            elif pos == 4:
                plt.title(f'Average Score per Number of Tasks for Fourth Place per Series {title}', fontsize = 20)
                plt.xlim(0, 3.3)
            else:
                plt.title(f'Average Score per Number of Tasks for Last Place per Series {title}', fontsize = 20)
                plt.xlim(0, 3)

        if average_type == 'episode':
            plt.xlabel('Average Score per Number of Episodes', fontsize = 18)
            if pos == 1:
                plt.title(f'Average Score per Number of Episodes for First Place per Series {title}', fontsize = 20)        
                plt.xlim(0, 21)
            elif pos == 2:
                plt.title(f'Average Score per Number of Episodes for Second Place per Series {title}', fontsize = 20)
                plt.xlim(0, 20)
            elif pos == 3:
                plt.title(f'Average Score per Number of Episodes for Third Place per Series {title}', fontsize = 20)
                plt.xlim(0, 19)
            elif pos == 4:
                plt.title(f'Average Score per Number of Episodes for Fourth Place per Series {title}', fontsize = 20)
                plt.xlim(0, 18)
            else:
                plt.title(f'Average Score per Number of Episodes for Last Place per Series {title}', fontsize = 20)
                plt.xlim(0, 17)
        
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)

        plt.show()


def plot_contestent_scores(position_tables, colour_list, average_type, top = True, top_n = 20, bottom = False, 
                               bottom_n = 1):
    
    position_tables = position_tables.sort_values(by = 'Score', ascending = False).reset_index(drop = True)

    fig, axes = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.2)

    if top == True:
        position_tables = position_tables[20 - top_n : 21] 
        position_tables = position_tables.sort_values(by = 'Score', ascending = True).reset_index(drop = True)
     
        title = f'(Top {top_n})'
        
    if bottom == True:
        position_tables = position_tables.sort_values(by = 'Score', ascending = True).reset_index(drop = True)
        position_tables = position_tables[0 : bottom_n]
        title = f'(Bottom {bottom_n})'

    if average_type == 'total':
        for i, score, name, series, seat, colour in zip(range(0, 21), position_tables['Score'],
                            position_tables['Name'], 
                            position_tables['Series'],
                            position_tables['Seat'],  colour_list):
                print(i)
                plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
                plt.text(score + 1, i, str(score), va='center', fontsize = 15, color = colour)  
                plt.text(5, i, str(series), va = 'center', fontsize = 12, color = 'white')
                plt.text(20, i, str(seat), va = 'center', fontsize = 12, color = 'white')
        plt.xlim(0, 205)
        plt.title(f'Final Scores of {title} Contestents Across all Series', fontsize = 20)   
        plt.xlabel('Total Score', fontsize = 18)

    if average_type == 'task':
        for i, score, name, series, seat, colour in zip(range(1, 21), position_tables['Score'],
                            position_tables['Name'], 
                            position_tables['Series'],
                            position_tables['Seat'],  colour_list):
            plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
            plt.text(score + 0.25, i-1, str(score), va='center', fontsize = 15, color = colour)  
            plt.text(0.5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
            plt.text(1.6, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')
        plt.xlabel('Average Score per Number of Tasks', fontsize = 18)
        plt.title(f'Average Score per Number of Tasks of {title} Contestents Across all Series', fontsize = 20)        
        plt.xlim(0, 4)
    if average_type == 'episode':
        for i, score, name, series, seat, colour in zip(range(1, 21), position_tables['Score'],
                            position_tables['Name'], 
                            position_tables['Series'],
                            position_tables['Seat'],  colour_list):
            plt.barh(y = name, width = score, color = colour, edgecolor = 'black')
            plt.text(score + 1, i-1, str(score), va='center', fontsize = 15, color = colour)  
            plt.text(2.5, i-1, str(series), va = 'center', fontsize = 12, color = 'white')
            plt.text(7.5, i-1, str(seat), va = 'center', fontsize = 12, color = 'white')
        plt.xlabel('Average Score per Number of Episodes', fontsize = 18)
        plt.title(f'Average Score per Number of Episodes of {title} Contestents Across all Series', fontsize = 20)        
        plt.xlim(0, 22)

    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)

    plt.show()