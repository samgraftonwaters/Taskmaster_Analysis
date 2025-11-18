import pandas as pd
import numpy as np
import Total_Scores_EDA as TSE

def count_DQ_all_contestents(file_path:str, table_name:str, number_series:int):
    
    count_dq = []

    for series in range(1, number_series+1):

        data = pd.read_excel(file_path + table_name, sheet_name = f'Series_{series}')
        cols = data.columns

        series_contestents = data[cols[4:9]]

        dq_count_values = series_contestents.eq('DQ').sum().values
        dq_count_index = series_contestents.eq('DQ').sum().index

        name_DQ = {}
        for i, j in zip(dq_count_index, dq_count_values):
            name_DQ.update({i : j})

        count_dq.append(name_DQ)

    dq_df_cols = [(name, score) for d in count_dq for name, score in d.items()]

    dq_df = pd.DataFrame(dq_df_cols, columns = ['Name', 'DQ'])
    dq_df["Series"] = [f"S{(i // 5) + 1}" for i in range(len(dq_df))]

    return(dq_df)

def dq_total_per_series(dataframe):

    total_dq = []
    for series in range(1, 21):

        series_df = dataframe[dataframe['Series'] == f'S{series}']

        series_totals = series_df['DQ'].sum()

        total_dq.append([f'S{series}', series_totals])

    total_dq_series = pd.DataFrame(total_dq, columns = ['Series', 'Total DQ'])

    return(total_dq_series)

# print(final_positions_dq.columns)

# print(final_positions_dq[final_positions_dq['Series'] == 'S1'][['Name', 'DQ','Total Score', 'Position', 'Total Missed Scores', 'New Position',
#        'Position Difference']].head(30))

# sns.scatterplot(x = final_positions_dq['Avg_Task_Score'], y = final_positions_dq['Total Score'], 
#                 hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Avgerage Score per Number of Tasks', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Total Score'], 
#                 hue = final_positions_dq['Position'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Total Score', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

# sns.scatterplot(x = final_positions_dq['DQ'], y = final_positions_dq['Position'], 
#                 hue = final_positions_dq['Total Score'], size = final_positions_dq['Seat'])
# plt.xticks(fontsize = 14)
# plt.yticks(ticks = [5, 4, 3, 2, 1], labels = ['5th', '4th', '3rd', '2nd', '1st'], fontsize = 14)
# plt.gca().invert_yaxis()
# plt.xlabel('Number of Disqualifications', fontsize = 15)
# plt.ylabel('Final Position', fontsize = 15)
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 14)
# plt.show()

