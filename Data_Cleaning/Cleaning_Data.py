import pandas as pd
import numpy as np

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

def get_data(filepath, filename, sheetname, number_tables = None):

    if number_tables == None:
        data = pd.read_excel(filepath + filename, sheet_name = sheetname)
    
    else:
        data = []
        for tables in range(1, number_tables):
            data_tabs = pd.read_excel(filepath + filename, sheet_name = f'Series_{tables}')
            data.append(data_tabs)
    return(data)


df = get_data(filepath = file_path, filename='Taskmaster_CoC_Scores.xlsx', sheetname='Series', number_tables=3)

print(df[0])

# df = pd.DataFrame()

# df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Bonus').replace('T', 'Tie Break')

# df = df.drop(columns = ["Episode"], axis = 1)
# eps_task = df['Task ID'].str.split('-', expand = True)
# df['Episode'] = eps_task[0]
# df['Episode'] = df['Episode'].str.replace('Episode ', 'Ep')
# # df['Series'] = f"S{series}"

# task_type = df['Description'].str.split(":", expand = True)

# df['Team Task'] = np.where(task_type[0] == 'Team', 1, 0)
# df['Prize Task'] = np.where(task_type[0] == 'Prize', 1, 0)
# df['Live Task'] = np.where(task_type[0] == 'Live', 1, 0)
# df['Tie Break'] = np.where(df['Task Number'] == 'T', 1, 0)
# df['Bonus Task'] = np.where(df['Description'].str.contains('Bonus'), 1, 0)
# df['Extra Part'] = np.where(df['Task Number'].str.contains('Extra'), 1, 0)

# # df[cols[4:]] = df[cols[4:]].replace('DQ', np.nan)

# # for contestent in cols[4:]:
# # df[contestent] = pd.to_numeric(df[contestent], errors='coerce')

# df = df.drop(columns = ["Task ID"], axis = 1)