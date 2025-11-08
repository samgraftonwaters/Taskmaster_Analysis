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
