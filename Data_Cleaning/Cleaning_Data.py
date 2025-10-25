import pandas as pd
import numpy as np
import Cleaning_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'


df = CF.get_data(filepath = file_path, filename='Taskmaster_CoC_Scores.xlsx', sheetname='Series', number_tables=3)

print(df[0])

