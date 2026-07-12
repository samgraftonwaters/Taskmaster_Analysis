import pandas as pd
import numpy as np
from Function_Scripts import EDA_Functions as EF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
scores_series_table = file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx'

Total_per_series = []
Total_per_episode = []
Total_per_task = []

number_of_series = 21

for series in range(1, number_of_series + 1):

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

#Total scores for all series
Total_per_series = EF.total_score_tables(table = Total_per_series, extra_columns=['Series'], drop_total = False)
Total_per_episode = EF.total_score_tables(table = Total_per_episode, extra_columns=['Series', 'Number of Episodes'])
Total_per_task = EF.total_score_tables(table = Total_per_task, extra_columns=['Series', 'Number of Tasks'])

print(Total_per_series)
print(Total_per_task)

series_all_totals = pd.concat([Total_per_series[['Series', 'Total']], Total_per_task['Number of Tasks'],
                               Total_per_episode['Number of Episodes']], axis = 1)

series_all_totals['Total per Number of Episodes'] = Total_per_series['Total'] / Total_per_episode['Number of Episodes']
series_all_totals['Total per Number of Tasks'] = Total_per_series['Total'] / Total_per_task['Number of Tasks']

print(series_all_totals.head())
print(named_series_table)

#Highest and lowest scores and averages per epsiodes or tasks for each seat
total_highest_seat = EF.find_highest_seat(value_table = Total_per_series, name_table = named_series_table)
total_lowest_seat = EF.find_lowest_seat(value_table = Total_per_series, name_table = named_series_table)
episodes_highest_seat = EF.find_highest_seat(value_table = Total_per_episode, name_table = named_series_table)
episodes_lowest_seat = EF.find_lowest_seat(value_table = Total_per_episode, name_table = named_series_table)
tasks_highest_seat = EF.find_highest_seat(value_table = Total_per_task, name_table = named_series_table)
tasks_lowest_seat = EF.find_lowest_seat(value_table = Total_per_task, name_table = named_series_table)

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
final_scores_ordered_seats = EF.final_score_seat_positions(score_table = Total_per_series, 
                                                        name_table = named_series_table)

final_scores_players = final_scores_ordered_seats

average_tasks_ordered_seats = EF.final_score_seat_positions(score_table = Total_per_task , 
                                                            name_table = named_series_table, contain_summed_total = False)

average_tasks_players = average_tasks_ordered_seats

average_episodes_ordered_seats = EF.final_score_seat_positions(score_table = Total_per_episode , 
                                                            name_table = named_series_table, contain_summed_total = False)
average_episodes_players = average_episodes_ordered_seats

total_score_positions_ordered = EF.ordering_final_scores_all_positions(datafame = final_scores_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'], 
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                        positions = [5, 4, 3, 2, 1], order_col = 'Score', order = True)


total_score_positions_unordered = EF.ordering_final_scores_all_positions(datafame = final_scores_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'], 
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                       positions = [5, 4, 3, 2, 1], order_col = 'Score', order = False)


average_episode_positions_ordered = EF.ordering_final_scores_all_positions(datafame = average_episodes_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'],
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                        positions = [5, 4, 3, 2, 1], order_col = 'Score', order = True)
print(average_episode_positions_ordered)

average_episode_positions_unordered = EF.ordering_final_scores_all_positions(datafame = average_episodes_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'], 
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                        positions = [5, 4, 3, 2, 1], order_col = 'Score', order = False)

average_tasks_positions_ordered = EF.ordering_final_scores_all_positions(datafame = average_tasks_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'], 
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                        positions = [5, 4, 3, 2, 1], order_col = 'Score', order = True)
print(average_tasks_positions_ordered)

average_tasks_positions_unordered = EF.ordering_final_scores_all_positions(datafame = average_tasks_players, 
                                       series_col = 'Series', 
                                       name_cols = ['Fifth Place Name', 'Fourth Place Name', 
                                                    'Third Place Name', 'Second Place Name', 'First Place Name'],
                                        score_cols = ['Fifth Place Score', 'Fourth Place Score', 
                                                      'Third Place Score', 'Second Place Score', 'First Place Score'], 
                                        seat_cols = ['Fifth Place Seat', 'Fourth Place Seat', 'Third Place Seat', 
                                                    'Second Place Seat', 'First Place Seat'],
                                        positions = [5, 4, 3, 2, 1], order_col = 'Score', order = False)



total_score_positions_ordered.to_csv(output_path + 'Total Final Scores and Positions.csv', sep = ',', index = False, encoding="utf-8")
average_tasks_positions_ordered.to_csv(output_path + 'Avg Task Scores and Positions.csv', index = False, sep = ',')
average_episode_positions_ordered.to_csv(output_path + 'Avg Episode Scores and Positions.csv', index = False, sep = ',')
total_scores_all_series.to_csv(output_path + 'Summary Scores and Averages Per Seat.csv', sep = ',', index = False)
Total_per_series.to_csv(output_path + 'Total Scores for each Series.csv', index = False, sep = ',')
Total_per_episode.to_csv(output_path + 'Total Scores per Number of Episodes.csv', index = False, sep = ',')
Total_per_task.to_csv(output_path + 'Total Scores per Number of Tasks.csv', index = False, sep = ',')