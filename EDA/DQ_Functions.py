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

