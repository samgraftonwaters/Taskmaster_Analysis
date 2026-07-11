import pandas as pd
import numpy as np

def clean_numerical(file_path, file_name, number_sheets, output_filename):

    """
    Cleans the scraped data for each series.

    Parameters:
    ----------
        file_path (str): filepath to the raw data
        file_name (str): name of Excel file with all Series' data
        number_sheets (int): number of sheets to iterate over.
        output_filename (str): name of of the cleaned Excel workbook
    
    Returns:
    --------
        Excel workbook with each Series' cleaned data on each tab
    
    """

    with pd.ExcelWriter(file_path + output_filename + '.xlsx') as writer:
    
        for series in range(1,number_sheets+1) if number_sheets > 1 else range(20+number_sheets, 20+number_sheets+1):

            data = pd.read_excel(file_path + file_name + '.xlsx', sheet_name = 'Series_' + str(series))

            df = pd.DataFrame(data)

            cols = df.columns

            df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Solo').replace('T', 'Tie Break')
            
            df = df.drop(columns = ["Episode"], axis = 1)
            eps_task = df['Task ID'].str.split('-', expand = True)
            
            df['Episode'] = eps_task[0]
            df['Episode'] = df['Episode'].str.replace('Episode ', 'Ep')
            df['Series'] = f"S{series}"

            task_type =  df['Description'].str.split(":", expand = True)

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

            df = df.drop(columns = ["Task ID"], axis = 1)
            cols = df.columns
            df[cols[2:7]] = df[cols[2:7]].apply(pd.to_numeric, errors='coerce')
            df[cols[10:]] = df[cols[10:]].apply(pd.to_numeric, errors='coerce')

            df.to_excel(writer, sheet_name = f'Series_{series}', index = False)



def seat_to_name(file_path, file_name, number_sheets):

    """
    Maps each Series' seat number to its respective contestents' name

    Parameters:
    -----------
        file_path (str): filepath to the raw data
        file_name (str): name of Excel file with all Series' data
        number_sheets (int): number of sheets to iterate over.
    
    Returns:
    --------
        dataframe with contestants' names (rows) under their respective seat number (columns)
    """

    clean_table_cols = []
    for series in range(1,number_sheets+1) if number_sheets > 1 else range(20+number_sheets, 20+number_sheets+1):

        dataframe = pd.read_excel(file_path + file_name + '.xlsx', sheet_name = f'Series_{series}')

        cols = dataframe.columns

        contestents = cols[2:7]

        df = pd.DataFrame(columns=[contestents])

        clean_cols = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        clean_table_cols.append(clean_cols)

    new_cols = [f"Seat Name {i+1}" for i in range(5)]

    new_df = pd.DataFrame(clean_table_cols, columns=new_cols)

    new_df = new_df.astype(str)

    return(new_df)