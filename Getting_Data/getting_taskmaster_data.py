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
url = "https://taskmaster.fandom.com/wiki/Series_1"
header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}


if SF.scrape_with_requests(url, headers = header) == 'error':
    soup = SF.scrape_with_selenium(url)
    print('scrape with selenium')
else:
    soup = SF.scrape_with_requests(url, headers = header)
    print('scrape with requests')

soup_output = soup.prettify()

# with open('taskmaster_series_1.txt', 'w') as f:
#     f.write(soup.prettify())


# <table class="tmtable">

series_1 = soup.find_all('table', class_='tmtable')


table = soup.find('table', class_='tmtable')


# df = pd.DataFrame(columns = ['Task', 'Description', 'Frank Skinner', 'Josh Widdicombe',
#                                    'Roisin Conaty', 'Romesh Ranganathan', 'Tim Key'])

# Create DataFrame
df = SF.extracting_table(table = table)

print(df.info())
print(df.head(10))


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

    print(' ')
    print(f'series {series}')
    print(df.head())

# contestents = ['Frank Skinner', 'Josh Widdicombe','Roisin Conaty', 'Romesh Ranganathan', 'Tim Key']
# df[contestents] = df[contestents].replace('✘', 0).replace('–', 0).replace('✔', 1)#.replace('\u2013', 0, inplace = True).replace('\u2718', 0, inplace = True)

# # Preview
# print(df.head(10))

# df.to_csv('series_1_output.csv', sep = ',', index=False)




# # Collecting Ddata
# for row in table.tbody.find_all('tr'):    
#     # Find all data for each column
#     columns = row.find_all('td')

#     print(row, columns)
    
#     if(columns != []):
#         Task = columns[0].text.strip()
#         Description = columns[1].text.strip()
#         Seat1 = columns[2].span.contents[0].strip('&0.')
#         Seat2 = columns[3].span.contents[0].strip('&0.')
#         Seat3 = columns[4].span.contents[0].strip('&0.')
#         Seat4 = columns[5].span.contents[0].strip('&0.')
#         Seat5 = columns[6].span.contents[0].strip('&0.')

#         df = df.append({'Task': Task,  'Description': Description, 'Frank Skinner': Seat1, 
#                         'Josh Widdicombe': Seat2, 'Roisin Conaty' : Seat3, 'Romesh Ranganathan' : Seat4,
#                          'Tim Key' : Seat5}, ignore_index=True)

# df.head()
# print(series_1)

# with open('series_1_table.txt', 'w') as f:
#     f.write(str(series_1))

# tables = soup.select('table', attrs={"class":"hauptlink"})

# print(tables)

# table = []
# for tr in soup.find('table', class_='tmtable').find_all('tr'):
#     row = [td.text for td in tr.find_all('td')]
#     # If want to filter out all except LA then can do that here
#     if len(row) == 3:
#         table.append(row)
# df = pd.DataFrame(table, columns=['Task', 'Description', 'Frank Skinner', 'Josh Widdicombe',
#                                    'Roisin Conaty', 'Romesh Ranganathan', 'Tim Key'])

# print(df)