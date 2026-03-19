import pandas as pd
import Text_Cleaning as TC


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())

cleaned_tasks = TC.clean_task_description(task_description_text = task_description)

print(cleaned_tasks)