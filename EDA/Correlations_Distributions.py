import pandas as pd
import numpy as np
import DQ_Exploration as DQE
import Total_Scores_EDA as TSE

import matplotlib.pyplot as plt
import seaborn as sns


sns.scatterplot(x = DQE.final_positions_dq['Avg_Task_Score'], y = DQE.final_positions_dq['Total Score'], 
                hue = DQE.final_positions_dq['Position'], size = DQE.final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

sns.scatterplot(x = DQE.final_positions_dq['DQ'], y = DQE.final_positions_dq['Total Score'], 
                hue = DQE.final_positions_dq['Position'], size = DQE.final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Total Score', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()

sns.scatterplot(x = DQE.final_positions_dq['DQ'], y = DQE.final_positions_dq['Position'], 
                hue = DQE.final_positions_dq['Total Score'], size = DQE.final_positions_dq['Seat'])
plt.xticks(fontsize = 14)
plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
plt.gca().invert_yaxis()
plt.xlabel('Number of Disqualifications', fontsize = 15)
plt.ylabel('Final Position', fontsize = 15)
plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
plt.show()


######
# plot distributions of total scores, team scores etc
# plot total scores against vs team A and team B scores, and all player scores based on those from team tasks
# plot correlation plots
# Determine correlations and R_squared values for above plots
