import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

input_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

data = pd.read_csv(input_path + 'Full Contestent Table.csv')

print(data.head())
print(data.info())

data_nums = data.select_dtypes(include=[float, int])

columns = data_nums.columns

non_normal = []
normal = []

for cols in columns:
    norm = stats.normaltest(data_nums[cols])
    if norm.pvalue < 0.01:
        non_normal.append(cols)
        print(f'{cols} p-value = {norm.pvalue}')
    else:
        normal.append(cols)
        print(f'{cols} p-value = {norm.pvalue}')

print(non_normal)
print(len(non_normal))

print(normal)
print(len(normal))

# for cols in non_normal:
#     plt.hist(data_nums[cols])
#     plt.title(f'{cols}', fontsize = 20)
#     plt.show()

# for cols in normal:
#     plt.hist(data_nums[cols])
#     plt.title(f'{cols}', fontsize = 20)
#     plt.show()

correlations = data_nums.corr(method = 'spearman')
print(correlations)
print(correlations.columns)

print(correlations.stack())

high_corr = (
    correlations.where(np.triu(np.ones(correlations.shape), k=1).astype(bool))  # keep upper triangle only
    .stack()                                                 # convert to pairs
    .reset_index()
)

high_corr.columns = ['var_1', 'var_2', 'correlation']

result_high = high_corr[high_corr['correlation'].abs() > 0.7]

print(result_high)
print(len(result_high))

result_low = high_corr[(high_corr['correlation'].abs() <= 0.7) & ((high_corr['correlation'].abs() > 0.4))]

print(result_low)
print(len(result_low))
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