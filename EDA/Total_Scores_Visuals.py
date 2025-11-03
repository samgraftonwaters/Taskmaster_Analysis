import Total_Scores_EDA as TSE

import seaborn as sns
import matplotlib.pyplot as plt

print(TSE.seat_winners)

seat_winners = TSE.seat_winners.groupby('Seat Winner').count().reset_index()


seat_losers = TSE.seat_losers.groupby('Seat Loser').count().reset_index()

sns.barplot(data = seat_winners)
plt.show()
sns.barplot(data = seat_losers)
plt.show()