import pandas as pd
import numpy as np

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

# fig = plt.figure()
# ax1 = fig.subplots()
# ax2 = ax1.twiny()

# ax1.barh(y_values-0.2, dq_change_plus['Total Missed Scores'], height = 0.4, color = 'white', edgecolor = 'blue')
# ax1.barh(y_values+0.2, dq_change_plus['Total Score'], height = 0.4, color = 'white', edgecolor = 'green')

# ax1.barh(y_values-0.2, -dq_change_minus['Total Missed Scores'], height = 0.4, color = 'white', edgecolor = 'red')
# ax1.barh(y_values+0.2, -dq_change_minus['Total Score'], height = 0.4, color = 'white', edgecolor = 'darkorange')


# # ax1.vlines(x=dq_change_plus['Total Score'], ymin=y_values - 0, ymax=y_values +0.4, linewidth=3, color = 'blue')
# # ax1.vlines(x=dq_change_plus['Total Missed Scores'], ymin=y_values - 0.4, ymax=y_values +0, linewidth=3, color = 'green')

# # ax1.vlines(x=dq_change_minus['Total Score'], ymin=y_values - 0, ymax=y_values +0.4, linewidth=3, color = 'red')
# # ax1.vlines(x=-dq_change_minus['Total Missed Scores'], ymin=y_values - 0.4, ymax=y_values +0, linewidth=3, color = 'darkorange')

# for (y, name_plus, score_plus, missed_score_plus, 
#               name_minus, score_minus, missed_score_minus) in zip(y_values, dq_change_plus['Name'], dq_change_plus['Total Score'],
#                                                                   dq_change_plus['Total Missed Scores'], dq_change_minus['Name'], 
#                                                                   dq_change_minus['Total Score'], dq_change_minus['Total Missed Scores']):
    
# #     ax1.text(score_plus-100, y-0.2, name_plus, fontsize = 12, color = 'blue')
# #     ax1.text(score_minus+100, y-0.2, name_minus, fontsize = 12, color = 'red')
#     ax1.text(score_plus, y-0.1, name_plus, fontsize = 14, color = 'blue')
#     ax1.text(score_minus, y-0.1, name_minus, fontsize = 14, color = 'red')

#     ax1.text(score_plus+2, y+0.15, str(round(score_plus,2)), fontsize = 14, color = 'blue')
#     ax1.text(missed_score_plus+2, y-0.3, str(missed_score_plus), fontsize = 14, color = 'green')

#     ax1.text(-score_minus, y+0.2, str(round(score_minus,2)), fontsize = 14, color = 'red')
#     ax1.text(-missed_score_minus, y-0.3, str(missed_score_minus), fontsize = 14, color = 'darkorange')


# ax2.plot(dq_change_plus['Position Difference'], y_values, marker = 'o', markersize = 15, color = 'darkgreen', linestyle='')
# ax2.plot(dq_change_minus['Position Difference'], y_values, marker = 'o', markersize = 15, color = 'darkred', linestyle='')

# # ax1.invert_yaxis()
# # ax2.invert_yaxis()

# ax1.tick_params(axis='x', labelsize=14)
# # ax1.set_xticks([-200, -150, -100, -50, 0, 50, 100, 150, 200])
# # ax1.set_xlim(-260, 260)
# ax2.tick_params(axis='x', labelsize=14)
# ax2.set_xticks([-1, 1])
# ax1.set_xlabel('Total Score', fontsize = 20)
# ax1.set_ylabel('Series', fontsize = 20)
# ax2.set_xlabel('Position Difference', fontsize = 20)
# ax1.set_yticks(ticks = y_values, labels = dq_change_plus['Series'].unique(), fontsize = 14)
# plt.show()