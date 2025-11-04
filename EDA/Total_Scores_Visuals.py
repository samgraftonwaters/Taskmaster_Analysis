import Total_Scores_EDA as TSE

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#### Visual Settings
# plt.style.use('ggplot')

## other settings, e.g.
plt.rcParams['figure.figsize'] = (13, 7)


#Number of times each seat won or lost over all series of Taskmaster

plt.bar(x = TSE.seat_winners['Seat Number']-0.2, height = TSE.seat_winners['Count Winners'], 
        label = 'Number of Wins', width = 0.40, color = 'blue', alpha = 0.6, edgecolor ='black')
plt.bar(x = TSE.seat_losers['Seat Number']+0.2, height = TSE.seat_losers['Count Losers'], 
        label = 'Number of Loses', width = 0.40, color = 'green', alpha = 0.6, edgecolor ='black')

for i in range(5):
    plt.text(i+0.8, TSE.seat_winners['Count Winners'][i]+0.05, 
             TSE.seat_winners['Count Winners'][i], ha='center', fontsize = 15, color = 'blue')
    plt.text(i+1.2, TSE.seat_losers['Count Losers'][i]+0.05, 
             TSE.seat_losers['Count Losers'][i], ha='center', fontsize = 15, color = 'green')

plt.title('The number of wins or loses per seat in all 20 Series of Taskmaster', fontsize = 16)
plt.xlabel('Seat Number', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.legend(loc = 'best', fontsize = 15)
plt.show()

##Total scores and averages for all series summed/combined

#Total

plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[0]].values[0][0:5], 
        label = 'Number of Wins', width = 0.5, color = 'blue', alpha = 0.6, edgecolor ='black')

for i in range(5):
    plt.text(i+1, TSE.total_scores_all_series.iloc[[0]].values[0][0:5][i]+0.5, 
             TSE.total_scores_all_series.iloc[[0]].values[0][0:5][i], ha='center', fontsize = 15, color = 'blue')

plt.hlines(TSE.total_scores_all_series.iloc[[0]].values[0][6], 0, 6, lw = 5, linestyle = '--',
           label = f'Average = {TSE.total_scores_all_series.iloc[[0]].values[0][6]}', color = 'purple')

plt.title('The Total Score per seat in all 20 Series of Taskmaster', fontsize = 16)
plt.ylim(2700, 2820)
plt.xlim(0.5, 5.5)
plt.xlabel('Seat Number', fontsize = 14)
plt.ylabel('Total Score', fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.legend(loc = 'best', fontsize = 15)
plt.show()

#Per number of Episodes

plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[1]].values[0][0:5], 
        label = 'Number of Wins', width = 0.5, color = 'green', alpha = 0.6, edgecolor ='black')

for i in range(5):
    plt.text(i+1, TSE.total_scores_all_series.iloc[[1]].values[0][0:5][i]+0.1, 
             TSE.total_scores_all_series.iloc[[1]].values[0][0:5][i], ha='center', fontsize = 15, 
             color = 'green')

plt.hlines(TSE.total_scores_all_series.iloc[[1]].values[0][6], 0, 6, lw = 5, linestyle = '--',
           label = f'Average = {TSE.total_scores_all_series.iloc[[1]].values[0][6]}', color = 'red')

plt.title('The Total Score per Number of Episodes for each seat in all 20 Series of Taskmaster', fontsize = 16)
plt.ylim(14, 16)
plt.xlim(0.5, 5.5)
plt.xlabel('Seat Number', fontsize = 14)
plt.ylabel('Total Score per Number of Episodes', fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.legend(loc = 'best', fontsize = 15)
plt.show()

#Per number of Tasks
plt.bar(x = range(1,6), height = TSE.total_scores_all_series.iloc[[2]].values[0][0:5], 
        label = 'Number of Wins', width = 0.5, color = 'orange', alpha = 0.6, edgecolor ='black')

for i in range(5):
    plt.text(i+1, TSE.total_scores_all_series.iloc[[2]].values[0][0:5][i]+0.012, 
             TSE.total_scores_all_series.iloc[[2]].values[0][0:5][i], ha='center', fontsize = 15, 
             color = 'darkorange')

plt.hlines(TSE.total_scores_all_series.iloc[[2]].values[0][6], 0, 6, lw = 5, linestyle = '--',
           label = f'Average = {TSE.total_scores_all_series.iloc[[2]].values[0][6]}', color = 'blue')

plt.title('The Total Score per Number of Tasks for each seat in all 20 Series of Taskmaster', fontsize = 16)
plt.ylim(2.5, 2.7)
plt.xlim(0.5, 5.5)
plt.xlabel('Seat Number', fontsize = 14)
plt.ylabel('Total Score per Number of Tasks', fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.legend(loc = 'best', fontsize = 15)
plt.show()