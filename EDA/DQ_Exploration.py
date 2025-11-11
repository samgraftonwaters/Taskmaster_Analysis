import pandas as pd
import numpy as np

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

named_series_table = pd.read_csv(file_path + 'seat_contestent_series_table.csv')
series_tables = file_path + 'Taskmaster_Series_Scores.xlsx'

count_dq = []

for series in range(1, 21):

    data = pd.read_excel(series_tables, sheet_name = f'Series_{series}')
    cols = data.columns

    series_contestents = data[cols[4:9]]

    dq_count = series_contestents.eq('DQ').sum().to_frame().T.reset_index(drop = True) #value_counts()['DQ']

    dq_count['Series'] = f'S{series}'

    count_dq.append(dq_count)

for i in range(len(count_dq)):
    if i < len(count_dq)-1:
        print(i)
        first = count_dq[i]
        second = count_dq[i+1]
        final = pd.concat([first, second])
    else:
        final = pd.concat([final, count_dq[i]])

print(final.reset_index())
