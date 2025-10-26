import pandas as pd
import numpy as np
import Cleaning_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

# cleaned_data = CF.clean_numerical(file_path = file_path, file_name = 'Taskmaster_Series_Scores', 
#                 sheet_name = 'Series', number_sheets = 20, output_filename = 'Taskmaster_Series_Scores_Cleaned')


# seat_contestent_table = []
# for series in range(1, 21):

#     cleaned_data = pd.read_excel(file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx', sheet_name = f'Series_{series}')

#     seat_table = CF.seat_to_name(dataframe = cleaned_data)

#     seat_table['Series'] = f'S{series}'

#     seat_contestent_table.append(seat_table)

seat_contestent_table = CF.seat_to_name(file_path = file_path, file_name = 'Taskmaster_Series_Scores_Cleaned')

seat_contestent_table["Series"] = "S" + (seat_contestent_table.index + 1).astype(str)
    
print(seat_contestent_table)


seat_contestent_table.to_csv(file_path + 'seat_contestent_series_table.csv', index = False, sep = ',')



