import pandas as pd
import numpy as np

def get_data(filepath, filename, sheetname, number_tables = None):

    if number_tables == None:
        data = pd.read_excel(filepath + filename, sheet_name = sheetname)
    
    else:
        data = []
        for tables in range(1, number_tables):
            data_tabs = pd.read_excel(filepath + filename, sheet_name = f'Series_{tables}')
            data.append(data_tabs)
    return(data)



def clean_numerical(file_path, file_name, sheet_name, number_sheets):
    
    for series in sheet_name + number_sheets:

        data = pd.read_excel(file_path + file_name, sheet_name = series)

        df = pd.DataFrame(data)

        cols = df.columns

        df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Bonus').replace('T', 'Tie Break')

        df = df.drop(columns = ["Episode"], axis = 1)
        eps_task = df['Task ID'].str.split('-', expand = True)
        df['Episode'] = eps_task[0]
        df['Episode'] = df['Episode'].str.replace('Episode ', 'Ep')
        # df['Series'] = f"S{series}"

        task_type = df['Description'].str.split(":", expand = True)

        df['Team Task'] = np.where(task_type[0] == 'Team', 1, 0)
        df['Prize Task'] = np.where(task_type[0] == 'Prize', 1, 0)
        df['Live Task'] = np.where(task_type[0] == 'Live', 1, 0)
        df['Tie Break'] = np.where(df['Task Number'] == 'T', 1, 0)
        df['Bonus Task'] = np.where(df['Description'].str.contains('Bonus'), 1, 0)
        df['Extra Part'] = np.where(df['Task Number'].str.contains('Extra'), 1, 0)

        df[cols[4:]] = df[cols[4:]].replace('DQ', 0)

        for contestent in cols[4:]:
            df[contestent] = pd.to_numeric(df[contestent], errors='coerce')

        df = df.drop(columns = ["Task ID"], axis = 1)