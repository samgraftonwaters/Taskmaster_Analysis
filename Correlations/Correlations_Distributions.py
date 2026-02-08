import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
 '#7f7f7f', '#bcbd22', '#17becf']

input_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

data = pd.read_csv(input_path + 'Full Contestent Table.csv')
data = data.rename(columns = {'DQ' : 'Disqualifications'})

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

result_high_var1 = result_high['var_1'].unique()
result_high_var2 = result_high['var_2'].unique()

result_high_var1 = []
result_high_var2 = []

for num, i in enumerate(np.array(result_high['var_1'].unique())):
    result_high_var1.append([num, i])
for num, j in enumerate(np.array(result_high['var_2'].unique())):
    result_high_var2.append([num, j])

result_high_var1 = pd.DataFrame(np.vstack(result_high_var1), columns = ['x_axis', 'var_1'])
result_high_var2 = pd.DataFrame(np.vstack(result_high_var2), columns = ['y_axis', 'var_2'])

result_high = pd.merge(result_high, result_high_var1, on = 'var_1', how = 'left')
result_high = pd.merge(result_high, result_high_var2, on = 'var_2', how = 'left')
result_high['x_axis'] = result_high['x_axis'].astype(int)
result_high['y_axis'] = result_high['y_axis'].astype(int)

var1_labels = result_high['var_1'].str.replace(' ', '\n').str.replace('_', '\n')
print(var1_labels)

print(result_high.info())
print(result_high)

high_colour = result_high["correlation"]

# center the colormap at 0
norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

# choose a diverging colormap
cmap = plt.cm.coolwarm

# map correlations to RGBA colors
result_high["color"] = high_colour.apply(lambda x: cmap(norm(x)))

print(result_high)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.15, top = 0.92, left = 0.2, right = 0.98)
for i in range(len(result_high)):
    text = plt.text(result_high.iloc[i]['x_axis'], result_high.iloc[i]['y_axis'], 
             f"{result_high.iloc[i]['correlation']:.2f}", fontsize = 15,
               ha="center", va="center", color="white",
               bbox=dict(boxstyle="round,pad=0.3",
                fc=result_high.iloc[i]["color"],
                ec="black",
                lw=0.7,
                alpha=0.9))
plt.xlim(-0.5, 9.5)
plt.ylim(-0.5, 11.5)
plt.xticks(result_high['x_axis'], var1_labels, fontsize = 12)
plt.yticks(result_high['y_axis'], result_high['var_2'], fontsize = 12)
plt.title('Highest Correlated Variables (corr > 0.7)', fontsize = 20)
plt.grid(True, linestyle="--", alpha=0.3)
#colour bar
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, label="Correlation")
cbar.set_label("Correlation", fontsize=14)
cbar.ax.tick_params(labelsize=12)
plt.show()

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