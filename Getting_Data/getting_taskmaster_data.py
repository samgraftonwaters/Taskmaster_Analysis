import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
import pandas as pd
import scraping_functions as SF
import numpy as np
import re

output_filepath = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

#Main Series
with pd.ExcelWriter(output_filepath + 'Taskmaster_Series_Scores.xlsx') as writer:
    for series in range(1, 21):

        url = f"https://taskmaster.fandom.com/wiki/Series_{series}"
        header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

        result = SF.scrape_with_requests(url, headers=header)

        if result == 'error':
            soup = SF.scrape_with_selenium_imdb(url)
            print('scrape with selenium')
        else:
            soup = result
            print('scrape with requests')

        table = soup.find('table', class_='tmtable')

        for t in soup.find_all('table'):
            print(t.get('class'))

        df = SF.extracting_table(table = table)
        cols = df.columns

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'Series_{series}', index = False)

        time.sleep(5)

#Champion of Champions
champ_of_champs = ['', '_2', "_3", "_4"]
with pd.ExcelWriter(output_filepath + 'Taskmaster_CoC_Scores.xlsx') as writer:
    
    for series in champ_of_champs:

        url = f"https://taskmaster.fandom.com/wiki/Champion_of_Champions{series}"

        result = SF.scrape_with_requests(url, headers=header)

        if result == 'error':
            soup = SF.scrape_with_selenium_imdb(url)
            print('scrape with selenium')
        else:
            soup = result
            print('scrape with requests')

        table = soup.find('table', class_='tmtable')

        print(table)

        df = SF.extracting_table(table = table)
        cols = df.columns

        print(df)

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'CoC_{series}', index = False)

        time.sleep(5)


#New Years Treats
url = f"https://taskmaster.fandom.com/wiki/Taskmaster%27s_New_Year_Treat"

result = SF.scrape_with_requests(url, headers=header)

if result == 'error':
    soup = SF.scrape_with_selenium_imdb(url)
    print('scrape with selenium')
else:
    soup = result
    print('scrape with requests')

tables = soup.find_all('table', class_='tmtable')

with pd.ExcelWriter(output_filepath + 'Taskmaster_NewYears_Scores.xlsx') as writer:
    for series, table in zip(range(1,7), tables):
        df = SF.extracting_table(table = table)
        cols = df.columns

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'NYT_{series}', index = False)

        time.sleep(5)
