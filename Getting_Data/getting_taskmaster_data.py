import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
import pandas as pd
import scraping_functions as SF
import numpy as np
import re


# URL to scrape
url = "https://taskmaster.fandom.com/wiki/Series_2"
header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}


if SF.scrape_with_requests(url, headers = header) == 'error':
    soup = SF.scrape_with_selenium(url)
    print('scrape with selenium')
else:
    soup = SF.scrape_with_requests(url, headers = header)
    print('scrape with requests')

soup_output = soup.prettify()

# with open('taskmaster_series_2.txt', 'w') as f:
#      f.write(soup.prettify())

series_1 = soup.find_all('table', class_='tmtable')

table = soup.find('table', class_='tmtable')

with open('taskmaster_series_8.txt', 'w') as f:
     f.write(str(table))

df = SF.extracting_table(table = table)

cols = df.columns

print(df.head(50))

# df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Bonus').replace('T', 'Tie Break')

# # df = df.drop(columns = ["Episode"], axis = 1)
# eps_task = df['Task ID'].str.split('-', expand = True)
# df['Eps'] = eps_task[0]
# df['Eps'] = df['Eps'].str.replace('Episode ', 'Ep')
# df['Series'] = f"S2"

# task_type = df['Description'].str.split(":", expand = True)

# df['Team Task'] = np.where(task_type[0] == 'Team', 1, 0)

# df[cols[4:]] = df[cols[4:]].replace('DQ', np.nan)

# for contestent in cols[4:]:
#     df[contestent] = pd.to_numeric(df[contestent], errors='coerce')

# df = df.drop(columns = ["Task ID"], axis = 1)

# print(df.head())
# print(df.info())   

# df.to_csv('Series_2_output.csv', index = False, sep = ',')

# with pd.ExcelWriter('Taskmaster_Series_Scores.xlsx') as writer:
#     for series in range(1, 21):

#         url = f"https://taskmaster.fandom.com/wiki/Series_{series}"
#         header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}


#         if SF.scrape_with_requests(url, headers = header) == 'error':
#             soup = SF.scrape_with_selenium(url)
#             print('scrape with selenium')
#         else:
#             soup = SF.scrape_with_requests(url, headers = header)
#             print('scrape with requests')

#         table = soup.find('table', class_='tmtable')

#         df = SF.extract_taskmaster_table(table = table)
#         cols = df.columns

#         df['Tasknumber'] = df['Task Number'].replace('1', 'Prize').replace('S', 'Bonus').replace('T', 'Tie Break')

#         # df = df.drop(columns = ["Episode"], axis = 1)
#         eps_task = df['Task ID'].str.split('-', expand = True)
#         df['Episode'] = eps_task[0]
#         df['Episode'] = df['Episode'].str.replace('Episode ', 'Ep')
#         df['Series'] = f"S{series}"

#         task_type = df['Description'].str.split(":", expand = True)

#         df['Team Task'] = np.where(task_type[0] == 'Team', 1, 0)
#         df['Prize Task'] = np.where(task_type[0] == 'Prize', 1, 0)
#         df['Live Task'] = np.where(task_type[0] == 'Live', 1, 0)
#         df['Tie Break'] = np.where(df['Task Number'] == 'T', 1, 0)
#         df['Bonus Task'] = np.where(df['Description'].str.contains('Bonus'), 1, 0)

#         df[cols[4:]] = df[cols[4:]].replace('DQ', np.nan)

#         for contestent in cols[4:]:
#             df[contestent] = pd.to_numeric(df[contestent], errors='coerce')

#         # df = df.drop(columns = ["Task ID"], axis = 1)
#         print(' ')
#         print(f'series {series}')
#         print(df.head())
#         print(df.info())    

#         df.to_excel(writer, sheet_name = f'Series_{series}', index = False)

