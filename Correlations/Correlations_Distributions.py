import pandas as pd
import numpy as np
from scipy import stats

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
data.columns = data.columns.str.replace('_', ' ')

print(data.head())
print(data.info())

data_nums = data.select_dtypes(include=[float, int])
data_nums = data_nums.drop(['Team of'], axis = 1)

normal_variables, non_normal_variables = CF.normal_variables(data_table = data_nums)

correlations = data_nums.corr(method = 'spearman')
print(correlations)
print(correlations.columns)

grouped_variables = CF.group_corr_variables(correlations = correlations)

result_high = CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.7)

result_high_var1 = CF.axis_values_for_variables(data_table = result_high, variable_column = 'var_1',
                                             axis_column = 'x_axis')
result_high_var2 = CF.axis_values_for_variables(data_table = result_high, variable_column = 'var_2',
                                             axis_column = 'y_axis')

result_high = pd.merge(result_high, result_high_var1, on = 'var_1', how = 'left')
result_high = pd.merge(result_high, result_high_var2, on = 'var_2', how = 'left')

var1_labels_high = result_high['var_1'].str.replace(' ', '\n').str.replace('Percentage', '%').str.replace(' per ', ' ')
result_high['var_2'] = result_high['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')
print(result_high)

result_high, cmap, norm = CF.set_correlation_colours(data_table = result_high, corr_column = 'correlation', limits = 1)

CF.correlation_compare_plot(data_table = result_high, xaxis_column = 'x_axis', yaxis_column = 'y_axis',
                            correlation_column = 'correlation', var1_labels = var1_labels_high, 
                            var2_column = 'var_2', title = 'Highest Correlated Variables (corr > 0.7)',
                            cmap = cmap, norm = norm)

result_low = CF.set_corr_thresholds(corr_data = grouped_variables, range = True, threshold = [0.4, 0.7])

result_low_var1 = CF.axis_values_for_variables(data_table = result_low, variable_column = 'var_1',
                                             axis_column = 'x_axis')
result_low_var2 = CF.axis_values_for_variables(data_table = result_low, variable_column = 'var_2',
                                             axis_column = 'y_axis')

result_low = pd.merge(result_low, result_low_var1, on = 'var_1', how = 'left')
result_low = pd.merge(result_low, result_low_var2, on = 'var_2', how = 'left')

var1_labels_low = result_low['var_1'].str.replace(' ', '\n').str.replace('Percentage', '%').str.replace(' per ', ' ')
result_low['var_2'] = result_low['var_2'].str.replace('Percentage', '%').str.replace(' per ', ' ')
print(result_low)

result_low, cmap, norm = CF.set_correlation_colours(data_table = result_low, corr_column = 'correlation', limits = 0.7)

CF.correlation_compare_plot(data_table = result_low, xaxis_column = 'x_axis', yaxis_column = 'y_axis',
                            correlation_column = 'correlation', var1_labels = var1_labels_low, 
                            var2_column = 'var_2', title = 'Medium Correlated Variables (0.4 < corr < 0.7)',
                            cmap = cmap, norm = norm)



# sns.scatterplot(x = DQE.final_positions_dq['Avg_Task_Score'], y = DQE.final_positions_dq['Total Score'], 
#                 hue = DQE.final_positions_dq['Position'], size = DQE.final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = DQE.final_positions_dq['DQ'], y = DQE.final_positions_dq['Total Score'], 
#                 hue = DQE.final_positions_dq['Position'], size = DQE.final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = DQE.final_positions_dq['DQ'], y = DQE.final_positions_dq['Position'], 
#                 hue = DQE.final_positions_dq['Total Score'], size = DQE.final_positions_dq['Seat'])
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