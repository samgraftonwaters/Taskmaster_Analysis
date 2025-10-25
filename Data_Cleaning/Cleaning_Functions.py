import pandas as pd
import numpy as np

def get_data(filepath, filename, sheetname, number_tables = None):

    if number_tables == None:
        data = pd.read_excel(filepath + filename, sheet_name = sheetname)
        return(data)
    
    else:
        data = []
        for tables in range(1, number_tables):
            data_tabs = pd.read_excel(filepath + filename, sheet_name = f'Series_{tables}')
            data.append(data_tabs)
        return(data)



def clean_numerical(file_path, file_name, sheet_name, number_sheets, output_filename):

    with pd.ExcelWriter(file_path + output_filename + '.xlsx') as writer:
    
        for series in range(1,number_sheets+1):

            data = pd.read_excel(file_path + file_name + '.xlsx', sheet_name = sheet_name + "_" + str(series))

            df = pd.DataFrame(data)

            cols = df.columns

            df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Solo').replace('T', 'Tie Break')

            df = df.drop(columns = ["Episode"], axis = 1)
            eps_task = df['Task ID'].str.split('-', expand = True)
            df['Episode'] = eps_task[0]
            df['Episode'] = df['Episode'].str.replace('Episode ', 'Ep')
            # df['Series'] = f"S{series}"

            task_type = df['Description'].str.split(":", expand = True)

            df = df.replace('Grand Total', f'Series {series} Grand Total')
            df = df.replace('Season Total', f'Series {series} Total')

            df['Team Task'] = np.where(task_type[0] == 'Team', 1, 0)
            df['Prize Task'] = np.where(task_type[0] == 'Prize', 1, 0)
            df['Live Task'] = np.where(task_type[0] == 'Live', 1, 0)
            df['Tie Break'] = np.where(df['Task Number'] == 'T', 1, 0)
            df['Solo Task'] = np.where(df['Description'].str.contains('Solo'), 1, 0)
            df['Extra Part'] = np.where(df['Task Number'].str.contains('Extra'), 1, 0)

            df[cols[4:]] = df[cols[4:]].replace('DQ', 0)
            df[cols[4:]] = df[cols[4:]].replace('-', 0)

            # for contestent in cols[4:]:
            #     df[contestent] = pd.to_numeric(df[contestent], errors='coerce')

            df = df.drop(columns = ["Task ID"], axis = 1)

            print(df.head())

            df.to_excel(writer, sheet_name = f'Series_{series}', index = False)


def total_scores(dataframe, total, per_number_eps, per_number_tasks):

    dataframe = pd.DataFrame(dataframe)
    cols = dataframe.columns
    contestents = cols[2:7]
    
    total_score = dataframe[dataframe['Task Number'].str.contains('Grand Total')]

    if total == True:

        total = total_score[contestents]

        return(total)

    if per_number_eps == True:

        number_eps = dataframe['Episode'].isin(['Ep','Total']).count()

        total_per_number_eps = total_score / number_eps

        return(total_per_number_eps)
    
    if per_number_tasks == True:

        number_tasks = dataframe[dataframe['Episode'].str.contains('Total') == False].count()

        total_per_number_tasks = total_score / number_tasks

        return(total_per_number_tasks)