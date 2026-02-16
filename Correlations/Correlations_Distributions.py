import pandas as pd
import numpy as np
from scipy import stats
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
import seaborn as sns

import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

input_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

data = pd.read_csv(input_path + 'Full Contestent Table.csv')
data = data.rename(columns = {'DQ' : 'Disqualifications'})
data['Seat Num'] = data['Seat'].str.replace('Seat ', '').astype(int)
data.columns = data.columns.str.replace('_', ' ')

print(data.head())
print(data.info())

data_nums = data.select_dtypes(include=[float, int])

normal_variables, non_normal_variables = CF.normal_variables(data_table = data_nums)

normal_variables.to_csv(input_path + 'Normal Variable Comparison Table.csv', sep = ',', index = False)
non_normal_variables.to_csv(input_path + 'Non-Normal Variable Comparison Table.csv', sep = ',', index = False)

correlations = data_nums.corr(method = 'spearman')
print(correlations)
print(correlations.columns)

correlations.to_csv(input_path + 'All Numerical Correlations.csv', sep = ',', index = False)

grouped_variables = CF.group_corr_variables(correlations = correlations)

#high correlations

result_high = CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.7)

result_high_var1 = CF.axis_values_for_variables(data_table = result_high, variable_column = 'var_1',
                                             axis_column = 'x_axis')
result_high_var2 = CF.axis_values_for_variables(data_table = result_high, variable_column = 'var_2',
                                             axis_column = 'y_axis')

result_high = pd.merge(result_high, result_high_var1, on = 'var_1', how = 'left')
result_high = pd.merge(result_high, result_high_var2, on = 'var_2', how = 'left')

result_high, cmap, norm = CF.set_correlation_colours(data_table = result_high, corr_column = 'correlation', limits = 1)
result_high_corrs = result_high.copy()

var1_labels_high = result_high['var_1'].str.replace(' ', '\n').str.replace('Percentage', '%').str.replace(' per ', ' ')
result_high['var_2'] = result_high['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')
print(result_high)
result_high.to_csv(input_path + 'Highly (>0.7) Correlated Variables.csv', sep = ',', index = False)

CF.correlation_compare_plot(data_table = result_high, xaxis_column = 'x_axis', yaxis_column = 'y_axis',
                            correlation_column = 'correlation', var1_labels = var1_labels_high, 
                            var2_column = 'var_2', title = 'Highest Correlated Variables (corr > 0.7)',
                            cmap = cmap, norm = norm)

data.columns = data.columns.str.replace('Percentage', '%').str.replace(' per ', ' ')
result_high_corrs['var_1'] = result_high_corrs['var_1'].str.replace('Percentage', '%').str.replace(' per ', ' ')
result_high_corrs['var_2'] = result_high_corrs['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')

# result_high_corrs_split = result_high_corrs.iloc[:11]
# print(result_high_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_high_corrs_split)

# result_high_corrs_split = result_high_corrs.iloc[11:].reset_index(drop = True)
# print(result_high_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_high_corrs_split)

#medium Correlations

result_medium = CF.set_corr_thresholds(corr_data = grouped_variables, range = True, threshold = [0.4, 0.7])

result_medium_var1 = CF.axis_values_for_variables(data_table = result_medium, variable_column = 'var_1',
                                             axis_column = 'x_axis')
result_medium_var2 = CF.axis_values_for_variables(data_table = result_medium, variable_column = 'var_2',
                                             axis_column = 'y_axis')

result_medium = pd.merge(result_medium, result_medium_var1, on = 'var_1', how = 'left')
result_medium = pd.merge(result_medium, result_medium_var2, on = 'var_2', how = 'left')

var1_labels_medium = result_medium['var_1'].str.replace(' ', '\n').str.replace('Percentage', '%').str.replace(' per ', ' ')
result_medium['var_2'] = result_medium['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')

result_medium, cmap, norm = CF.set_correlation_colours(data_table = result_medium, corr_column = 'correlation', limits = 0.7)
print(result_medium)

result_medium.to_csv(input_path + 'Medium (0.4-0.7) Correlated Variables.csv', sep = ',', index = False)

CF.correlation_compare_plot(data_table = result_medium, xaxis_column = 'x_axis', yaxis_column = 'y_axis',
                            correlation_column = 'correlation', var1_labels = var1_labels_medium, 
                            var2_column = 'var_2', title = 'Medium Correlated Variables (0.4 < corr < 0.7)',
                            cmap = cmap, norm = norm)

result_medium_corrs = result_medium.copy()
result_medium_corrs['var_1'] = result_medium_corrs['var_1'].str.replace('Percentage', '%').str.replace(' per ', ' ')
result_medium_corrs['var_2'] = result_medium_corrs['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')

# result_medium_corrs_split = result_medium_corrs.iloc[0:12]
# print(result_medium_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_medium_corrs_split)

# result_medium_corrs_split = result_medium_corrs.iloc[12:24].reset_index(drop = True)
# print(result_medium_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_medium_corrs_split)

# result_medium_corrs_split = result_medium_corrs.iloc[24:36].reset_index(drop = True)
# print(result_medium_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_medium_corrs_split)

# result_medium_corrs_split = result_medium_corrs.iloc[36:48].reset_index(drop = True)
# print(result_medium_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_medium_corrs_split)

# result_medium_corrs_split = result_medium_corrs.iloc[48:].reset_index(drop = True)
# print(result_medium_corrs_split)
# CF.corr_subplots(data_table = data, corr_table = result_medium_corrs_split)

####
#Score vs Average Score Tasks (0.61)

def slope(y1, y2, x1, x2):
    y = y2 - y1
    x = x2 - x1
    m = y/x
    return(m)

def intercept(y1, x1, slope):
    b = y1 - x1*slope
    return(b)

    

scores = data[['Avg Score Tasks', 'Score', 'Position', 'Seat']]

m = slope(y1 = 80, y2 = 150,
          x1 = scores['Avg Score Tasks'].min(), x2 = scores['Avg Score Tasks'].max())

c = intercept(y1 = 80, x1 = scores['Avg Score Tasks'].min(), slope = m)

y = (scores['Avg Score Tasks'] * m) + c

sns.scatterplot(x = scores['Avg Score Tasks'], y = scores['Score'], 
                hue = scores['Position'], size = scores['Seat'])
sns.regplot(x = scores['Avg Score Tasks'], y = scores['Score'])
plt.plot(scores['Avg Score Tasks'], y, color = 'green', lw = 3)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

score_above_115 = scores[scores['Score'] > y][['Score', 'Avg Score Tasks']]
score_below_115 = scores[scores['Score'] <= y][['Score', 'Avg Score Tasks']]

above_115_corr = score_above_115.corr()
below_115_corr = score_below_115.corr()

print(scores[['Score', 'Avg Score Tasks']].corr())
print(above_115_corr)
print(below_115_corr)

sns.regplot(x = score_above_115['Avg Score Tasks'], y = score_above_115['Score'])
sns.regplot(x = score_below_115['Avg Score Tasks'], y = score_below_115['Score'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

#Average Score Tasks vs Average Score Episodes (0.61)

avg_scores = data[['Avg Score Tasks', 'Avg Score Episodes', 'Position', 'Seat']]
print(avg_scores)

m = slope(y1 = 14, y2 = 19,
          x1 = avg_scores['Avg Score Tasks'].min(), x2 = 2.6)

c = intercept(y1 = 14, x1 = avg_scores['Avg Score Tasks'].min(), slope = m)

y = (avg_scores['Avg Score Tasks'] * m) + c

sns.scatterplot(x = avg_scores['Avg Score Tasks'], y = avg_scores['Avg Score Episodes'], 
                hue = avg_scores['Position'], size = avg_scores['Seat'])
sns.regplot(x = avg_scores['Avg Score Tasks'], y = avg_scores['Avg Score Episodes'])
plt.plot(avg_scores['Avg Score Tasks'], y, color = 'green', lw = 3)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Avgerage Score per Number of Episodes', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()


score_below = avg_scores[avg_scores['Avg Score Episodes'] > y][['Avg Score Episodes', 'Avg Score Tasks']]
score_above = avg_scores[avg_scores['Avg Score Episodes'] <= y][['Avg Score Episodes', 'Avg Score Tasks']]

above_corr = score_above.corr()
below_corr = score_below.corr()

print(avg_scores[['Avg Score Episodes', 'Avg Score Tasks']].corr())
print(above_corr)
print(below_corr)

sns.regplot(x = score_above['Avg Score Tasks'], y = score_above['Avg Score Episodes'])
sns.regplot(x = score_below['Avg Score Tasks'], y = score_below['Avg Score Episodes'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Avgerage Score per Number of Episodes', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()



    # sns.scatterplot(x = data[result_high['var_1']][row], y = data[result_high['var_2']][row])
    # plt.xticks(fontsize = 14)
    # plt.yticks(fontsize = 14)
    # plt.xlabel(str(result_high['var_1'][row]), fontsize = 15)
    # plt.ylabel(str(result_high['var_2'][row]), fontsize = 15)
    # plt.show()

# sns.scatterplot(x = data['Disqualifications'], y = data['Score'], 
#                 hue = data['Position'], size = data['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = data['Disqualifications'], y = data['Position'], 
#                 hue = data['Score'], size = data['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
# plt.gca().invert_yaxis()
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Final Position', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()


######
# plot distributions of total scores, team scores etc
# plot total scores against vs team A and team B scores, and all player scores based on those from team tasks
# plot correlation plots
# Determine correlations and R_squared values for above plots


### TEAM CORRELATION PLOTS

# plt.plot(all_teams['Number'], all_teams['Team_A_per_person_task'], 'o')
# plt.plot(all_teams['Number'], all_teams['Team_B_per_person_task'], 'o')
# plt.show()

# plt.plot(all_teams['Team_A_per_person_task'], all_teams['Team_B_per_person_task'], 'o')
# plt.grid()
# plt.show()

# plt.plot(team_name_scores['Number'], team_name_scores['TeamScoresPersonTask'], 'o')
# plt.grid()
# plt.show()