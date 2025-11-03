import Total_Scores_EDA as TSE

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#### Visual Settings
# plt.style.use('ggplot')

## other settings, e.g.
plt.rcParams['figure.figsize'] = (10.0, 8.0)

print(TSE.seat_winners)

seat_winners = TSE.seat_winners.groupby('Seat Winner').count().reset_index()
seat_winners['Numbers'] = range(1, 6)
seat_winners.columns = ['Seat', 'Count Winners', 'Seat Number']
print(seat_winners)

seat_losers = TSE.seat_losers.groupby('Seat Loser').count().reset_index()
seat_losers['Numbers'] = range(1, 6)
seat_losers.columns = ['Seat', 'Count Losers', 'Seat Number']
print(seat_losers)

seats = pd.concat([seat_losers.drop('Seat', axis = 1), seat_winners.drop('Seat', axis = 1)], axis = 1)
print(seats)

sns.barplot(data = seat_winners, x = 'Seat Number', y = 'Count Winners', label = 'Number of Wins', width = 0.8)
sns.barplot(data = seat_losers, x = 'Seat Number', y = 'Count Losers', label = 'Number of Loses', width = 0.8)

plt.title('The number of wins or loses per seat in all 20 Series of Taskmaster', fontsize = 16)
plt.xlabel('Seat Number', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.show()

sns.barplot(data = seats, x = 'Numbers', y = 'Series', label = 'Number of Loses', width = 0.8)