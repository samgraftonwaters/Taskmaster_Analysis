import pandas as pd
import numpy as np
import Cleaning_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

CF.clean_numerical(file_path = file_path, file_name = 'Taskmaster_Series_Scores', 
                sheet_name = 'Series', number_sheets = 20, output_filename = 'Taskmaster_Series_Scores_Cleaned')

