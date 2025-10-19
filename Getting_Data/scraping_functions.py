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

    df = pd.DataFrame(data)

    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

    return(df)


def extracting_tables_new(table):

    rows = table.find_all('tr')
    header_cells = rows[0].find_all('th')
    contestants = [th.get_text(strip=True) for th in header_cells[2:]]

    data = []
    current_episode = ''
    task_id = 0
    current_task = None
    rows_to_skip = 0  # count of continuation rows if row span present

    for row in rows[1:]:
        if rows_to_skip > 0:
            # We are in a forced continuation due to rowspan
            rows_to_skip -= 1
            # treat as continuation of current task (see below)
            is_new_task = False
        else:
            row_class = row.get('class', [])

            if 'tmtableepisode' in row_class:
                current_episode = row.get_text(strip=True).split(' (')[0]
                task_id = 0
                current_task = None
                continue
            if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
                current_task = None
                continue

            cols = row.find_all(['td', 'th'])
            if len(cols) < 2:
                continue

            first_cell = cols[0]
            first_text = first_cell.get_text(strip=True)
            has_link = first_cell.find('a') is not None
            looks_like_number = re.match(r'^\d+$', first_text) is not None
            is_new_task = has_link or looks_like_number

        if is_new_task:
            # begin new task
            task_number = first_text
            description = cols[1].get_text(" ", strip=True)
            score_cells = cols[2:]
            scores = [sc.get_text(strip=True).replace('\xa0','') for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))

            task_id += 1
            task_key = f"{current_episode.split(':')[0]}-T{task_id}"
            current_task = {
                'Episode': current_episode,
                'Task Number': task_number,
                'Task ID': task_key,
                'Descriptions': [description],
                'Scores': [scores]
            }
            data.append(current_task)

            # check for rowspan on first cell
            if first_cell.has_attr('rowspan'):
                try:
                    span_count = int(first_cell['rowspan'])
                except ValueError:
                    span_count = 1
                # rows_to_skip = span_count - 1 means next (span_count‑1) rows are continuation
                rows_to_skip = span_count - 1

        else:
            # continuation row – belongs to current_task
            if current_task is None:
                continue
            cols = row.find_all(['td','th'])
            # Here description likely in cols[0], scores in cols[1:]
            description = cols[0].get_text(" ", strip=True)
            score_cells = cols[1:]
            scores = [sc.get_text(strip=True).replace('\xa0','') for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))

            current_task['Descriptions'].append(description)
            current_task['Scores'].append(scores)

    # Now consolidate identical to before
    final_data = []
    for task in data:
        merged_scores = {}
        for i, contestant in enumerate(contestants):
            all_scores = [row[i] if i < len(row) else None for row in task['Scores']]
            filtered = [s for s in all_scores if s not in (None, '')]
            if len(filtered) == 0:
                merged_scores[contestant] = None
            elif len(filtered) == 1:
                merged_scores[contestant] = filtered[0]
            else:
                merged_scores[contestant] = filtered
        final_data.append({
            'Episode': task['Episode'],
            'Task Number': task['Task Number'],
            'Task ID': task['Task ID'],
            'Description': " ".join(task['Descriptions']).strip(),
            **merged_scores
        })

    for task in final_data:
        print(f"{task['Task ID']} - {task['Episode']} - Task {task['Task Number']}")
        print("Description:", task['Description'])
        for c in contestants:
            print(f"  {c}: {task[c]}")
        print()


    df = pd.DataFrame(final_data)

    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

    return(df)



def extracting_tables_newer(table):
    def get_clean_score(td):
        # Remove any footnote tags (e.g. <sup>, <small>)
        for sup in td.find_all(['sup', 'small']):
            sup.decompose()
        text = td.get_text(strip=True).replace('\xa0', '')
        return text if text != '' else None

    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    rows = table.find_all('tr')

    # header (contestants)
    header_cells = rows[0].find_all('th')
    contestants = [th.get_text(strip=True) for th in header_cells[2:]]

    data = []
    current_episode = ''
    task_id = 0
    current_task = None
    rows_to_skip = 0

    for idx, row in enumerate(rows[1:], start=1):
        row_class = row.get('class', [])
        
        # Episode row
        if 'tmtableepisode' in row_class:
            current_episode = row.get_text(strip=True).split(' (')[0]
            task_id = 0
            current_task = None
            continue
        
        # Skip total rows
        if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
            current_task = None
            continue

        # Now it's a task or continuation
        cols = row.find_all(['td', 'th'])
        if len(cols) < 2:
            print(f"Warning: skipped row {idx} (too few cols): {row}")
            continue

        first_cell = cols[0]
        first_text = first_cell.get_text(strip=True)
        has_link = first_cell.find('a') is not None
        looks_like_number = re.match(r'^\d+$', first_text) is not None

        if rows_to_skip > 0:
            # Forced continuation due to rowspan
            is_new = False
            rows_to_skip -= 1
        else:
            is_new = has_link or looks_like_number

        if is_new:
            # New task
            task_number = first_text
            desc = cols[1].get_text(" ", strip=True)
            score_cells = cols[2:]
            scores = [get_clean_score(sc) for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))

            task_id += 1
            task_key = f"{current_episode.split(':')[0]}-T{task_id}"
            current_task = {
                'Episode': current_episode,
                'Task Number': task_number,
                'Task ID': task_key,
                'Descriptions': [desc],
                'Scores': [scores]
            }
            data.append(current_task)

            # handle rowspan
            if first_cell.has_attr('rowspan'):
                try:
                    span = int(first_cell['rowspan'])
                except:
                    span = 1
                if span > 1:
                    rows_to_skip = span - 1

        else:
            # continuation row
            if current_task is None:
                print(f"Warning: continuation row but no current task at row {idx}: {row}")
                continue
            desc = first_text
            score_cells = cols[1:]
            scores = [get_clean_score(sc) for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))
            current_task['Descriptions'].append(desc)
            current_task['Scores'].append(scores)

    # Now consolidate
    final_data = []
    for task in data:
        merged = {}
        for i, name in enumerate(contestants):
            all_scores = [row[i] if i < len(row) else None for row in task['Scores']]
            filtered = [s for s in all_scores if s not in (None, '', '–', '-', 'DQ')]
            if len(filtered) == 0:
                merged[name] = None
            else:
                total = sum(safe_int(s) for s in filtered)
                merged[name] = total
        final_data.append({
            'Episode': task['Episode'],
            'Task Number': task['Task Number'],
            'Task ID': task['Task ID'],
            'Description': " ".join(task['Descriptions']).strip(),
            **merged
        })

    # Print tasks where any contestant score is None (to debug)
    for row in final_data:
        missing = [name for name in contestants if row.get(name) is None]
        if missing:
            print(f"Missing scores in {row['Task ID']} – contestants missing: {missing}")

    df = pd.DataFrame(final_data)
    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

    return df


def extracting_tables_newest(table):
    def get_clean_score(td):
        # Remove any footnote tags (e.g. <sup>, <small>)
        for sup in td.find_all(['sup', 'small']):
            sup.decompose()
        text = td.get_text(strip=True).replace('\xa0', '')
        return text if text != '' else None

    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    rows = table.find_all('tr')

    # header (contestants)
    header_cells = rows[0].find_all('th')
    contestants = [th.get_text(strip=True) for th in header_cells[2:]]

    data = []
    current_episode = ''
    task_id = 0
    current_task = None
    rows_to_skip = 0

    for idx, row in enumerate(rows[1:], start=1):
        row_class = row.get('class', [])
        
        # Episode row
        if 'tmtableepisode' in row_class:
            current_episode = row.get_text(strip=True).split(' (')[0]
            task_id = 0
            current_task = None
            continue
        
        # Skip total rows
        if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
            current_task = None
            continue

        # Now it's a task or continuation
        cols = row.find_all(['td', 'th'])
        if len(cols) < 2:
            print(f"Warning: skipped row {idx} (too few cols): {row}")
            continue

        first_cell = cols[0]
        first_text = first_cell.get_text(strip=True)
        has_link = first_cell.find('a') is not None
        looks_like_number = re.match(r'^\d+$', first_text) is not None

        if rows_to_skip > 0:
            # Forced continuation due to rowspan
            is_new = False
            rows_to_skip -= 1
        else:
            is_new = has_link or looks_like_number

        if is_new:
            # New task
            task_number = first_text
            desc = cols[1].get_text(" ", strip=True)
            score_cells = cols[2:]
            scores = [get_clean_score(sc) for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))

            task_id += 1
            task_key = f"{current_episode.split(':')[0]}-T{task_id}"
            current_task = {
                'Episode': current_episode,
                'Task Number': task_number,
                'Task ID': task_key,
                'Descriptions': [desc],
                'Scores': [scores]
            }
            data.append(current_task)

            # handle rowspan
            if first_cell.has_attr('rowspan'):
                try:
                    span = int(first_cell['rowspan'])
                except:
                    span = 1
                if span > 1:
                    rows_to_skip = span - 1

        else:
            # continuation row
            if current_task is None:
                print(f"Warning: continuation row but no current task at row {idx}: {row}")
                continue
            desc = first_text
            score_cells = cols[1:]
            scores = [get_clean_score(sc) for sc in score_cells]
            if len(scores) < len(contestants):
                scores += [None] * (len(contestants) - len(scores))
            current_task['Descriptions'].append(desc)
            current_task['Scores'].append(scores)

    # Now consolidate
    final_data = []
    for task in data:
        merged = {}
        for i, name in enumerate(contestants):
            all_scores = [row[i] if i < len(row) else None for row in task['Scores']]
            filtered = [s for s in all_scores if s not in (None, '', '–', '-', 'DQ')]
            if len(filtered) == 0:
                merged[name] = None
            else:
                total = sum(safe_int(s) for s in filtered)
                merged[name] = total
        final_data.append({
            'Episode': task['Episode'],
            'Task Number': task['Task Number'],
            'Task ID': task['Task ID'],
            'Description': " ".join(task['Descriptions']).strip(),
            **merged
        })

    # Print tasks where any contestant score is None (to debug)
    for row in final_data:
        missing = [name for name in contestants if row.get(name) is None]
        if missing:
            print(f"Missing scores in {row['Task ID']} – contestants missing: {missing}")

    df = pd.DataFrame(final_data)
    df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

    return df

