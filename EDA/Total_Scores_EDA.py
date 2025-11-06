import pandas as pd
import numpy as np
import EDA_Functions as EF

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
scores_series_table = file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx'

Total_per_series = []
Total_per_episode = []
Total_per_task = []

for series in range(1, 21):

    data = pd.read_excel(scores_series_table, sheet_name = f'Series_{series}')

    series_total = EF.total_scores(dataframe = data, total = True, per_number_eps = False, 
                                   per_number_tasks = False, include_col_names = False)
    Total_per_series.append(series_total)

    series_total_per_ep = EF.total_scores(dataframe = data, total = False, 
                                          per_number_eps = True, per_number_tasks = False, 
                                          include_col_names = False)
    Total_per_episode.append(series_total_per_ep)

    series_total_per_task = EF.total_scores(dataframe = data, total = False, 
                                            per_number_eps = False, per_number_tasks = True, 
                                            include_col_names = False)
    Total_per_task.append(series_total_per_task)

Total_per_series = EF.total_score_tables(table = Total_per_series, extra_columns=['Series'], drop_total = False)
Total_per_episode = EF.total_score_tables(table = Total_per_episode, extra_columns=['Series', 'Number of Episodes'])
Total_per_task = EF.total_score_tables(table = Total_per_task, extra_columns=['Series', 'Number of Tasks'])

total_highest_seat = EF.find_highest_seat(value_table = Total_per_series, name_table = named_series_table)
total_lowest_seat = EF.find_lowest_seat(value_table = Total_per_series, name_table = named_series_table)
episodes_highest_seat = EF.find_highest_seat(value_table = Total_per_episode, name_table = named_series_table)
episodes_lowest_seat = EF.find_lowest_seat(value_table = Total_per_episode, name_table = named_series_table)
tasks_highest_seat = EF.find_highest_seat(value_table = Total_per_task, name_table = named_series_table)
tasks_lowest_seat = EF.find_lowest_seat(value_table = Total_per_task, name_table = named_series_table)

print(total_highest_seat)
print(total_lowest_seat)
#Average scores and total scores per seat
total_scores_all_series = EF.total_scores_all_series(total_scores_df = Total_per_series, number_episodes_df = Total_per_episode,
                            number_tasks_df = Total_per_task)

####### Number of times each seat has won or lost a series of Taskmaster
seat_winners = EF.seat_winner_each_series(dataframe = Total_per_series)
seat_losers = EF.seat_loser_each_series(dataframe = Total_per_series)

seat_winners = seat_winners.groupby('Seat Winner').count().reset_index()
seat_winners['Numbers'] = range(1, 6)
seat_winners.columns = ['Seat', 'Count Winners', 'Seat Number']
seat_winners = seat_winners.drop('Seat', axis = 1)

seat_losers = seat_losers.groupby('Seat Loser').count().reset_index()
seat_losers['Numbers'] = range(1, 6)
seat_losers.columns = ['Seat', 'Count Losers', 'Seat Number']
seat_losers = seat_losers.drop('Seat', axis = 1)


######
final_scores_ordered_seats = EF.final_score_seat_orders(score_table = Total_per_series, name_table = named_series_table)

###
#Create Bump charts for all episode totals (and tasks) for each series: 
#https://towardsdatascience.com/create-bump-charts-with-matplotlib-431b0e6fcb90/
#https://medium.com/data-science/7-visualizations-with-python-to-express-changes-in-rank-over-time-71c1f11d7e4b
#https://stackoverflow.com/questions/68095438/how-to-make-a-bump-chart