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

GAF.age_series_stacked_bar(table = age_series)

print(gender_age_table[gender_age_table['Series'] == 'S14'])
print(final_scores[final_scores['Series'] == 'S14'])
print(episode_scores[episode_scores['Series'] == 'S14'])

final_scores_age_gender = pd.merge(left = final_scores, right = gender_age_table.drop('Series', axis = 1),
                                   on = 'Name', how = 'left')

final_scores_age_gender = pd.merge(left = final_scores_age_gender, 
                                   right = age_binned_table.drop(['Series Number', 'Age_at_First_Air'], axis = 1), 
                                   on = 'Name', how = 'left')

print(final_scores_age_gender)

# nans = final_scores_age_gender.index[final_scores_age_gender.isnull().any(1)]
# nan_rows = final_scores_age_gender.iloc[nans]
# print(nan_rows)
rows_with_all_nan = final_scores_age_gender[final_scores_age_gender.isna().any(axis=1)]
print(rows_with_all_nan)

seat_gender_table = final_scores_age_gender[['Seat', 'Gender']]
seat_gender_table['Seat'] = seat_gender_table['Seat'].str.replace('Seat ', '').astype(int)
print(seat_gender_table)

GAF.gender_count_series_bar(gender_age_table = seat_gender_table, series_seat = 'seat', 
                            title = 'Counts of Male and Female per Seat')