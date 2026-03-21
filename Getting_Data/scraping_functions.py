import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
        if response.status_code != 200:
            print("Bad status code:", response.status_code)
            return 'error'
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
    #pip install -U selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    print("Page loaded")
    html = driver.page_source
    driver.quit()
    print("Browser closed")
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
        
        if not row_class:
            cols = row.find_all(['td', 'th'])
            
            task_number = cols[0].get_text(strip=True)

            # Scores
            scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[2:]]

            # Pad scores if needed
            scores += [None] * (len(contestants) - len(scores))

            # Task ID for uniqueness
            task_id += 1
            if (description != '-') & (len(cols) > 6): 
                
                description = cols[1].get_text(strip=True)

                data.append({
                    'Episode': current_episode,
                    'Task Number': task_number,
                    'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                    'Description': description,
                    **{contestants[i]: scores[i] for i in range(len(contestants))}
                })
            elif  (len(cols) < 3): 
                
                description = cols[0].get_text(strip=True)

                data.append({
                    'Episode': current_episode,
                    'Task Number': 'Extra',
                    'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                    'Description': description,
                    **{contestants[i]: '-' for i in range(len(contestants))}
                })
            else:
                scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[1:]]
                scores += [None] * (len(contestants) - len(scores))
                description = cols[1].get_text(strip=True)

                data.append({
                    'Episode': current_episode,
                    'Task Number': 'Extra',
                    'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                    'Description': task_number,
                    **{contestants[i]: scores[i] for i in range(len(contestants))}
                })

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

            task_id += 1
            if (description != '-') & (len(cols) != 6):   
                data.append({
                    'Episode': current_episode,
                    'Task Number': task_number,
                    'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                    'Description': description,
                    **{contestants[i]: scores[i] for i in range(len(contestants))}
                })
            else:
                scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[1:]]
                scores += [None] * (len(contestants) - len(scores))

                data.append({
                    'Episode': current_episode,
                    'Task Number': 'Extra',
                    'Task ID': f"{current_episode.split(':')[0]}-T{task_id}",
                    'Description': task_number,
                    **{contestants[i]: scores[i] for i in range(len(contestants))}
                })
            
        elif 'tmtabletotal' in row_class:
            cols = row.find_all(['td', 'th'])

            total_scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[1:]]

            ep = f"{current_episode.split(':')[0]} Total"
            ep = ep.replace('Episode ', 'Ep')

            data.append({
                'Episode': current_episode,
                'Task Number': ep,
                'Task ID': ep,
                'Description': ep,
                **{contestants[i]: total_scores[i] for i in range(len(contestants))}
            })
        
        elif 'tmtablegrandtotal' in row_class:
            cols = row.find_all(['td', 'th'])

            grand_total = [td.get_text(strip=True).replace('\xa0', '') for td in cols[1:]]

            data.append({
                'Episode': 'Season Total',
                'Task Number': 'Grand Total',
                'Task ID': 'Grand Total',
                'Description': 'Grand Total',
                **{contestants[i]: grand_total[i] for i in range(len(contestants))}
            })

        # Skip total rows, etc.
        else:
            continue
    
    df = pd.DataFrame(data)
    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)
    for i in range(len(contestants)):
       
        df[contestants] = df[contestants].replace(r"(?<=\d)\[\d+\]", " ", regex=True)

    return df