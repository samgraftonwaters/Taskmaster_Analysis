import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver #pip install webdriver-manager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import undetected_chromedriver as uc
import pandas as pd


"""
Top two functions have been edited and changed slightly, but from: https://www.reddit.com/r/learnpython/comments/1ea3r0z/how_to_avoid_http_error_403_forbidden/
For the Selenium function, to connect to Chromedriver, I used help from: https://stackoverflow.com/questions/76928765/attributeerror-str-object-has-no-attribute-capabilities-in-selenium
For third function, the backbone was obtained from chatGPT, but editted for scraping infomation from ESPNCricinfo
"""

def scrape_with_requests(url):

    """
    Scrapes website using requests.

    Parameters:
    -----------
        url (str): website link

    Returns:
    --------
        Scraped webpage for analysis
    
    """

    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}
    try:
        session = requests.Session()
        response = session.get(url, headers=header)
        # response = requests.get(url, headers=headers)
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
def scrape_with_selenium_data(url):
    """
    Scrapes Taskmaster webpages using selenium to get data

    Parameters:
    -----------
        url (str): website link

    Returns:
    --------
        Scraped webpage for analysis
    
    """

    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        html = driver.page_source
    finally:
        driver.quit()
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, 'html.parser')

def scrape_with_selenium_imdb(url):

    """
    Scrapes IMDB webpages using selenium to get ratings

    Parameters:
    -----------
        url (str): website link

    Returns:
    --------
        Scraped webpage for analysis
    
    """
        
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
    finally:
        driver.quit()

    return BeautifulSoup(html, 'html.parser')


def extracting_table(table):

    """
    Takes the scraped webpage an gets the taskmaster tables over each series and each episode

    Parameters:
    -----------
        table: table within the scraped webpage to get all the information from it
    
    Returns:
    --------
        dataframe containing each epsisodes scoring table.
    
    """

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

def get_main_series_data_scraped(output_filepath, output_filename, start_series_number,
                                 final_series_number, single_series_number = None):
    
    """
    Scrape the taskmaster data for each requested series.

    Parameters:
    -----------
        output_filepath (str): filepath location to save the data to
        output_filename (str): name of final Excel workbook (excluding '.xlsx')
        start_series_number (int): series number to start iterating from
        final_series_number (int); series number to finish iterating to
        single_series_number (int): single series number to extract data for. Default is None

    Returns:
    --------
        Excel workbook with scraped data for each Serises in its own respective sheet
    """
    
    with pd.ExcelWriter(output_filepath + output_filename + '.xlsx') as writer:
        for series in range(start_series_number, final_series_number) if single_series_number is None else range(single_series_number, single_series_number + 1):

            url = f"https://taskmaster.fandom.com/wiki/Series_{series}"
            header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

            result = scrape_with_requests(url)

            if result == 'error':
                soup = scrape_with_selenium_imdb(url)
                print('scrape with selenium')
            else:
                soup = result
                print('scrape with requests')

            table = soup.find('table', class_='tmtable')

            for t in soup.find_all('table'):
                print(t.get('class'))

            df = extracting_table(table = table)
            cols = df.columns

            print(' ')
            print(f'series {series}')
            print(df.head())
            print(df.info())    

            df.to_excel(writer, sheet_name = f'Series_{series}', index = False)

            time.sleep(5)