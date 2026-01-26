import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import gender_age_functions as GAF

plt.rcParams['figure.figsize'] = (13, 7)

#Read in the data
file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

episode_scores = pd.read_csv(file_path + 'Episode Wins and Losses.csv', encoding="utf-8")
final_scores = pd.read_csv(file_path + 'Total Final Scores and Positions.csv', encoding="utf-8")

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv', encoding="utf-8")
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)

print(episode_scores.head())
print(final_scores.head())
print(gender_age_table.columns)

#Count number of gender and age groups per series
gender_count = GAF.gender_count_percent(gender_age_table)
gender_series = GAF.gender_count_series(gender_age_table)
GAF.gender_count_series_bar(gender_age_table = gender_age_table, series_seat = 'Series', 
                            title = 'Counts of Male and Female per Series')

age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_binned_table = GAF.setting_age_bins(table = age_table)

age_range_counts = GAF.age_range_metrics(table = age_binned_table)

age_series = GAF.age_group_series(table = age_binned_table)

GAF.age_series_stacked_bar(table = age_series, series_seat = 'Series', 
                           title = 'Number of Age Ranges for each Contestent per Series')

#Merge gender, age and total score tables together
final_scores_age_gender = GAF.merge_series_age_gender(series_table = final_scores, gender_table = gender_age_table, 
                        age_table = age_binned_table)

#Count number of gender and age groups per seat

seat_gender_table = GAF.seat_gender_metrics(datatable = final_scores_age_gender)

seat_age_table = GAF.seat_age_metrics(datatable = final_scores_age_gender)

GAF.gender_count_series_bar(gender_age_table = seat_gender_table, series_seat = 'seat', 
                            title = 'Counts of Male and Female per Seat')

GAF.age_series_stacked_bar(table = seat_age_table, series_seat = 'seat', 
                           title = 'Number of Age Ranges for each Seat')


print(final_scores_age_gender.head())

#Removed "non-binary" as only one contestent out of 100 who identifies, which makes the maths later more complex

final_scores_age_gender = final_scores_age_gender[final_scores_age_gender['Gender'] != 'Non-Binary']

#Created gender/age position tables for chi-squared and bias testing
position_gender_table = final_scores_age_gender[['Position', 'Gender', 'Score']]
position_age_table = final_scores_age_gender[['Position', 'Age_Ranges', 'Score']]

position_gender_count = position_gender_table.groupby(['Gender', 'Position'], observed=True)['Score'].sum().reset_index()
position_age_count = position_age_table.groupby(['Age_Ranges', 'Position'], observed=True)['Score'].sum().reset_index()

print(position_age_count)
print(position_gender_count)

#Carried out Chi-Squared Tests

age_chi2 = GAF.chi2_test(data_table = position_age_count, values = "Score", index = "Age_Ranges", 
                     columns = "Position", agg = "sum")

gender_chi2 = GAF.chi2_test(data_table = position_gender_count, values = "Score", index = "Gender", 
                     columns = "Position", agg = "sum")

# chi-squared result does not show Gender bias in Taskmaster scoring for gener.
# It shows that Gender and finishing position are statistically associated, but not by scoring bias.

# A chi-square test of independence showed a statistically significant association between Gender and position,
# χ²(8) = 1040.85, p < .001, indicating that the distribution of positions differs substantially across Gender 
# groups.

# So 1040.85 means:

# Across all Gender × position cells, the observed counts differ dramatically from what we’d expect 
# if Gender and position were unrelated.

#Carried out bias tests
grouped_ages = GAF.formatting_table(data_table = final_scores_age_gender)
grouped_ages_model = GAF.model_fitting(data_table = grouped_ages, target_variable = 'Score_Z', 
                  test_variables = ['Gender', 'Age_Ranges'])
GAF.anova_test(model = grouped_ages_model)

#
ages = GAF.formatting_table(data_table = final_scores_age_gender)
ages_model = GAF.model_fitting(data_table = grouped_ages, target_variable = 'Score_Z', 
                  test_variables = ['Gender', 'age_c'])
GAF.anova_test(model = ages_model)












