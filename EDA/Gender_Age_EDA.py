import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Function_Scripts import gender_age_functions as GAF

plt.rcParams['figure.figsize'] = (13, 7)

#Read in the data
file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

episode_scores = pd.read_csv(output_path + 'Episode Wins and Losses.csv', encoding="utf-8")
final_scores = pd.read_csv(output_path + 'Total Final Scores and Positions.csv', encoding="utf-8")

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv', encoding="utf-8")
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)

print(episode_scores.head())
print(final_scores.head())
print(gender_age_table.columns)

#Count number of gender and age groups per series
print('\n Gender Analysis \n')
gender_count = GAF.gender_count_percent(gender_age_table)
gender_series = GAF.gender_count_series(gender_age_table)
GAF.gender_count_series_bar(gender_age_table = gender_age_table, series_seat = 'Series', 
                            title = 'Counts of Male and Female per Series')

print('\n Age Analysis \n')
age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_binned_table = GAF.setting_age_bins(table = age_table)

age_range_counts = GAF.age_range_metrics(table = age_binned_table)

age_series = GAF.age_group_series(table = age_binned_table)

GAF.age_series_stacked_bar(table = age_series, series_seat = 'Series', 
                           title = 'Number of Age Ranges for each Contestent per Series')

print('\n Merging Tables \n')
#Merge gender, age and total score tables together
final_scores_age_gender = GAF.merge_series_age_gender(series_table = final_scores, gender_table = gender_age_table, 
                        age_table = age_binned_table)

#Count number of gender and age groups per seat
print('\n Seat Analysis \n')

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

#Carried out Chi-Squared Tests
print('\n Chi-Squared and Bias Testing \n')

age_chi2 = GAF.chi2_test(data_table = position_age_count, series_episode = 'series', values = "Score", 
                         index = "Age_Ranges", columns = "Position", agg = "sum")

gender_chi2 = GAF.chi2_test(data_table = position_gender_count, series_episode = 'series', values = "Score", 
                            index = "Gender", columns = "Position", agg = "sum")

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


#Epsisode Analysis
print('\n Episode Analysis \n')

episode_scores_age_gender = GAF.merge_series_age_gender(series_table = episode_scores, 
                                                        gender_table = gender_age_table.drop(['First_Air_Date', 'Birth_Date'], axis = 1),
                                                        age_table = age_binned_table)

eps_per_series = episode_scores_age_gender.groupby('Series')['Number_Episodes'].first().reset_index()
num_eps = eps_per_series['Number_Episodes'].sum()

episode_gender = episode_scores_age_gender.groupby('Gender', observed=True)[['Wins', 'Losses']].sum().reset_index()
episode_age = episode_scores_age_gender.groupby('Age_Ranges', observed=True)[['Wins', 'Losses']].sum().reset_index()

episode_gender['num'] = [1, 2, 3]
episode_age['num'] = range(1,6)
episode_age['Win Percentage'] = round((episode_age['Wins'] / num_eps *100), 2)
episode_age['Loss Percentage'] = round((episode_age['Losses'] / num_eps*100), 2)
episode_gender['Win Percentage'] = round((episode_gender['Wins'] / num_eps*100), 2)
episode_gender['Loss Percentage'] = round((episode_gender['Losses'] / num_eps*100), 2)
print(episode_gender)
print(episode_age)

#count/percentage bar charts for wins/losses split by age range or gender

GAF.episode_gender_age_bar(data_table = episode_gender, number_percentage = 'number', gender_age = 'gender', 
                       bartitle = 'Number of Wins and Losses for all Contestents a split by Gender')

GAF.episode_gender_age_bar(data_table = episode_gender, number_percentage = 'percentage', gender_age = 'gender', 
                       bartitle = 'Percentage of Wins and Losses for all Contestents a split by Gender')

GAF.episode_gender_age_bar(data_table = episode_age, number_percentage = 'number', gender_age = 'age', 
                       bartitle = 'Number of Wins and Losses for all Contestents a split by Age Range')

GAF.episode_gender_age_bar(data_table = episode_age, number_percentage = 'percentage', gender_age = 'age', 
                       bartitle = 'Percentage of Wins and Losses for all Contestents a split by Age Range')


#Chi Squared Analysis

episode_gender = episode_scores_age_gender[episode_scores_age_gender['Gender'] != 'Non-Binary'].groupby('Gender',observed=True)[['Wins', 'Losses']].sum()
episode_age = episode_scores_age_gender.groupby('Age_Ranges',observed=True)[['Wins', 'Losses']].sum()
print(episode_gender)
print(episode_age)

GAF.chi2_test(data_table = episode_gender, series_episode = 'episode', values = None, index = None, 
                     columns = None, agg = "sum")

GAF.chi2_test(data_table = episode_age, series_episode = 'episode', values = None, index = None, 
                     columns = None, agg = "sum")

final_scores_age_gender.to_csv(output_path + 'Gender_Age_Series_Scores.csv', index = False, sep = ',', encoding="utf-8")
episode_scores_age_gender.to_csv(output_path + 'Episode Scores per age and gender .csv', index = False, sep = ',', encoding="utf-8")
position_age_count.to_csv(output_path + 'Age Final Position Count.csv', index = False, sep = ',', encoding="utf-8")
position_gender_count.to_csv(output_path + 'Gender Final Position Count.csv', index = False, sep = ',', encoding="utf-8")