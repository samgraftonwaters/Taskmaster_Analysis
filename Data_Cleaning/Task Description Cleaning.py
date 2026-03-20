import pandas as pd
import numpy as np
import Cleaning_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

text_data = []

for series in range(1, 21):

    data = pd.read_excel(file_path + 'Taskmaster_Series_Scores_Cleaned.xlsx', sheet_name = "Series_" + str(series))

    data = pd.DataFrame(data)

    data = data[~data['Task Number'].str.contains('Total', na=False)]

    data = data[['Description', 'Episode', 'Series', 'Tasknumber', 'Team Task', 'Prize Task', 'Live Task']]

    text_data.append(data)


task_descriptions = pd.DataFrame(np.vstack(text_data), columns = ['Description', 'Episode', 'Series', 
                                                                  'Tasknumber', 'Team Task', 'Prize Task', 
                                                                  'Live Task'])

task_descriptions.to_csv(file_path + 'Script_Outputs/' + 'Task Descriptions Only.csv', sep = ',', index = False)