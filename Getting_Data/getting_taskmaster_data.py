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
url = f"https://taskmaster.fandom.com/wiki/Taskmaster%27s_New_Year_Treat"
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

# with open('taskmaster_new_years.txt', 'w') as f:
#      f.write(soup_output)

df = SF.extracting_table(table = table)

cols = df.columns

#Main Series
with pd.ExcelWriter('Taskmaster_Series_Scores.xlsx') as writer:
    for series in range(1, 21):

        url = f"https://taskmaster.fandom.com/wiki/Series_{series}"
        header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

        if SF.scrape_with_requests(url, headers = header) == 'error':
            soup = SF.scrape_with_selenium(url)
            print('scrape with selenium')
        else:
            soup = SF.scrape_with_requests(url, headers = header)
            print('scrape with requests')

        table = soup.find('table', class_='tmtable')

        df = SF.extracting_table(table = table)
        cols = df.columns

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'Series_{series}', index = False)

#Champion of Champions
champ_of_champs = ['', '_2', "_3"]
with pd.ExcelWriter('Taskmaster_CoC_Scores.xlsx') as writer:
    
    for series in champ_of_champs:

        url = f"https://taskmaster.fandom.com/wiki/Champion_of_Champions{series}"
        header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

        if SF.scrape_with_requests(url, headers = header) == 'error':
            soup = SF.scrape_with_selenium(url)
            print('scrape with selenium')
        else:
            soup = SF.scrape_with_requests(url, headers = header)
            print('scrape with requests')

        table = soup.find('table', class_='tmtable')

        df = SF.extracting_table(table = table)
        cols = df.columns

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'Series_{series}', index = False)


#New Years Treats
url = f"https://taskmaster.fandom.com/wiki/Taskmaster%27s_New_Year_Treat"
header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

if SF.scrape_with_requests(url, headers = header) == 'error':
    soup = SF.scrape_with_selenium(url)
    print('scrape with selenium')
else:
    soup = SF.scrape_with_requests(url, headers = header)
    print('scrape with requests')

tables = soup.find_all('table', class_='tmtable')

with pd.ExcelWriter('Taskmaster_NewYears_Scores.xlsx') as writer:
    for series, table in zip(range(1,6), tables):
        df = SF.extracting_table(table = table)
        cols = df.columns

        print(' ')
        print(f'series {series}')
        print(df.head())
        print(df.info())    

        df.to_excel(writer, sheet_name = f'Series_{series}', index = False)
