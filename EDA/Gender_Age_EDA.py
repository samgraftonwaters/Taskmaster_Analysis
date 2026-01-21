import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import gender_age_functions as GAF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

episode_scores = pd.read_csv(file_path + 'Episode Wins and Losses.csv', encoding="utf-8")
final_scores = pd.read_csv(file_path + 'Total Final Scores and Positions.csv', encoding="utf-8")

print(episode_scores.head())
print(final_scores.head())

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv', encoding="utf-8")
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)
print(gender_age_table.columns)

gender_count = GAF.gender_count_percent(gender_age_table)
gender_series = GAF.gender_count_series(gender_age_table)
GAF.gender_count_series_bar(gender_age_table = gender_age_table, series_seat = 'series', 
                            title = 'Counts of Male and Female per Series')

age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_binned_table = GAF.setting_age_bins(table = age_table)

age_range_counts = GAF.age_range_metrics(table = age_binned_table)

age_series = GAF.age_group_series(table = age_binned_table)

GAF.age_series_stacked_bar(table = age_series, series_seat = 'Series', 
                           title = 'Number of Age Ranges for each Contestent per Series')

final_scores_age_gender = GAF.merge_series_age_gender(series_table = final_scores, gener_table = gender_age_table, 
                        age_table = age_binned_table)

seat_gender_table = GAF.seat_gender_metrics(datatable = final_scores_age_gender)

seat_age_table = GAF.seat_age_metrics(datatable = final_scores_age_gender)

GAF.gender_count_series_bar(gender_age_table = seat_gender_table, series_seat = 'seat', 
                            title = 'Counts of Male and Female per Seat')

GAF.age_series_stacked_bar(table = seat_age_table, series_seat = 'seat', 
                           title = 'Number of Age Ranges for each Seat')