import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
import pandas as pd
import numpy as np
import re

"""
Top two functions have been edited and changed slightly, but from: https://www.reddit.com/r/learnpython/comments/1ea3r0z/how_to_avoid_http_error_403_forbidden/
For the Selenium function, to connect to Chromedriver, I used help from: https://stackoverflow.com/questions/76928765/attributeerror-str-object-has-no-attribute-capabilities-in-selenium
For third function, the backbone was obtained from chatGPT, but editted for scraping infomation from ESPNCricinfo
"""

def scrape_with_requests(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return('error')
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return('error')
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return('error')
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        return('error')

# Function to use Selenium for JavaScript rendered content
def scrape_with_selenium(url):
    cService = webdriver.ChromeService(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service = cService)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, 'html.parser')

def extracting_table(table):

    rows = table.find_all('tr')

    # Get contestant names from the header
    header_cells = rows[0].find_all('th')
    contestants = [th.get_text(strip=True) for th in header_cells[2:]]

    # Initialize
    data = []
    current_episode = ''
    task_id = 0

    for row in rows[1:]:
        row_class = row.get('class', [])

        # Episode row
        if 'tmtableepisode' in row_class:
            current_episode = row.get_text(strip=True).split(' (')[0]
            task_id = 0

        # Task row
        elif 'tmtablerow' in row_class:
            cols = row.find_all(['td', 'th'])

            # Skip malformed rows
            if len(cols) < 3:
                continue

            # Task number (can be "T", "S", etc.)
            task_number = cols[0].get_text(strip=True)
            description = cols[1].get_text(strip=True)

            # Scores
            scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[2:]]

            # Pad scores if needed
            scores += [None] * (len(contestants) - len(scores))

            # Task ID for uniqueness
            task_id += 1
            data.append({
                'Episode': current_episode,
                'Task Number': task_number,
                'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                'Description': description,
                **{contestants[i]: scores[i] for i in range(len(contestants))}
            })

        # Skip total rows, etc.
        else:
            continue

    print('contestents: ', contestants)

    df = pd.DataFrame(data)
    print(df)

    print(df.columns)

    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

    return(df)