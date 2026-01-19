import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import gender_age_functions as gaf


plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv')
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)
print(gender_age_table.columns)

gender_count = gaf.gender_count_percent(gender_age_table)
gender_series = gaf.gender_count_series(gender_age_table)
gaf.gender_count_series_bar(gender_age_table)

age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_table = age_table.copy()

age_bins = [20, 30, 40, 50, 60, 70]
age_labels = ['20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69']

age_table['Age_Ranges'] = pd.cut(age_table['Age_at_First_Air'], bins = age_bins, labels = age_labels, right = False)

age_ranges_count = age_table['Age_Ranges'].value_counts().reset_index()
age_ranges_count.columns = ['Age_Ranges', 'Count']
age_ranges_count['Percentage'] = (age_ranges_count['Count'] / age_ranges_count['Count'].sum()) * 100
print(age_ranges_count)

age_series = age_table.groupby('Series Number')['Age_Ranges'].value_counts().reset_index()
age_series = age_series.sort_values('Series Number', ascending = True)
print(age_series)


