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
        
        if '' in row_class:
            print(rows)

        # Task row
        elif 'tmtablerow' in row_class:
            cols = row.find_all(['td', 'th'])
            print(cols)

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
        
        elif 'tmtabletotal' in row_class:
            cols = row.find_all(['td', 'th'])

            total_scores = [td.get_text(strip=True).replace('\xa0', '') for td in cols[1:]]

            data.append({
                'Episode': current_episode,
                'Task Number': 'Total',
                'Task ID': 'Total',
                'Description': 'Total',
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
    
    # print('contestents: ', contestants)

    # print(data)
    # df = pd.DataFrame(data)
    # print(df)

    # print(df.columns)


#def extracting_tables(table):
#     def get_clean_score(td):
#         # Remove any footnote tags (e.g. <sup>, <small>)
#         for sup in td.find_all(['sup', 'small']):
#             sup.decompose()
#         text = td.get_text(strip=True).replace('\xa0', '')
#         return text if text != '' else None

#     def safe_int(val):
#         try:
#             return int(val)
#         except:
#             return 0

#     rows = table.find_all('tr')

#     # header (contestants)
#     header_cells = rows[0].find_all('th')
#     contestants = [th.get_text(strip=True) for th in header_cells[2:]]

#     data = []
#     current_episode = ''
#     task_id = 0
#     current_task = None
#     rows_to_skip = 0

#     for idx, row in enumerate(rows[1:], start=1):
#         row_class = row.get('class', [])
        
#         # Episode row
#         if 'tmtableepisode' in row_class:
#             current_episode = row.get_text(strip=True).split(' (')[0]
#             task_id = 0
#             current_task = None
#             continue
        
#         # Skip total rows
#         if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
#             current_task = None
#             continue

#         # Now it's a task or continuation
#         cols = row.find_all(['td', 'th'])
#         if len(cols) < 2:
#             print(f"Warning: skipped row {idx} (too few cols): {row}")
#             continue

#         first_cell = cols[0]
#         first_text = first_cell.get_text(strip=True)
#         has_link = first_cell.find('a') is not None
#         looks_like_number = re.match(r'^\d+$', first_text) is not None

#         if rows_to_skip > 0:
#             # Forced continuation due to rowspan
#             is_new = False
#             rows_to_skip -= 1
#         else:
#             is_new = has_link or looks_like_number

#         if is_new:
#             # New task
#             task_number = first_text
#             desc = cols[1].get_text(" ", strip=True)
#             score_cells = cols[2:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             if len(scores) < len(contestants):
#                 scores += [None] * (len(contestants) - len(scores))

#             task_id += 1
#             task_key = f"{current_episode.split(':')[0]}-T{task_id}"
#             current_task = {
#                 'Episode': current_episode,
#                 'Task Number': task_number,
#                 'Task ID': task_key,
#                 'Descriptions': [desc],
#                 'Scores': [scores]
#             }
#             data.append(current_task)

#             # handle rowspan
#             if first_cell.has_attr('rowspan'):
#                 try:
#                     span = int(first_cell['rowspan'])
#                 except:
#                     span = 1
#                 if span > 1:
#                     rows_to_skip = span - 1

#         else:
#             # continuation row
#             if current_task is None:
#                 print(f"Warning: continuation row but no current task at row {idx}: {row}")
#                 continue
#             desc = first_text
#             score_cells = cols[1:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             if len(scores) < len(contestants):
#                 scores += [None] * (len(contestants) - len(scores))
#             current_task['Descriptions'].append(desc)
#             current_task['Scores'].append(scores)

#     # Now consolidate
#     final_data = []
#     for task in data:
#         merged = {}
#         for i, name in enumerate(contestants):
#             all_scores = [row[i] if i < len(row) else None for row in task['Scores']]
#             filtered = [s for s in all_scores if s not in (None, '', '–', '-', 'DQ')]
#             if len(filtered) == 0:
#                 merged[name] = None
#             else:
#                 total = sum(safe_int(s) for s in filtered)
#                 merged[name] = total
#         final_data.append({
#             'Episode': task['Episode'],
#             'Task Number': task['Task Number'],
#             'Task ID': task['Task ID'],
#             'Description': " ".join(task['Descriptions']).strip(),
#             **merged
#         })

#     # Print tasks where any contestant score is None (to debug)
#     for row in final_data:
#         missing = [name for name in contestants if row.get(name) is None]
#         if missing:
#             print(f"Missing scores in {row['Task ID']} – contestants missing: {missing}")

#     df = pd.DataFrame(final_data)
#     df[contestants] = df[contestants].replace('✘', 0).replace('–', 0).replace('✔', 1)

#     return df

# #def combined(table):
#     def get_clean_score(td):
#         for tag in td.find_all(['sup', 'small']):
#             tag.decompose()
#         text = td.get_text(strip=True).replace('\xa0', '')
#         return text if text != '' else None

#     def safe_int(val):
#         try:
#             return int(val)
#         except:
#             return 0

#     rows = table.find_all('tr')
#     if not rows or len(rows[0].find_all('th')) < 3:
#         return pd.DataFrame()

#     header_cells = rows[0].find_all('th')
#     contestants = [th.get_text(strip=True) for th in header_cells[2:]]

#     data = []
#     current_episode = ''
#     task_id = 0
#     current_task = None
#     rows_to_skip = 0

#     for idx, row in enumerate(rows[1:], start=1):
#         row_class = row.get('class', [])

#         if 'tmtableepisode' in row_class:
#             current_episode = row.get_text(strip=True).split(' (')[0]
#             task_id = 0
#             current_task = None
#             continue

#         if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
#             continue

#         cols = row.find_all(['td', 'th'])
#         if len(cols) < 2:
#             continue

#         first_cell = cols[0]
#         first_text = first_cell.get_text(strip=True)
#         has_link = first_cell.find('a') is not None
#         looks_like_number = re.match(r'^[A-Za-z]$|^\d+$', first_text) is not None

#         if rows_to_skip > 0:
#             is_new = False
#             rows_to_skip -= 1
#         else:
#             is_new = has_link or looks_like_number

#         if is_new:
#             task_number = first_text
#             desc = cols[1].get_text(" ", strip=True)
#             score_cells = cols[2:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             scores += [None] * (len(contestants) - len(scores))

#             task_id += 1
#             task_key = f"{current_episode.split(':')[0]}-T{task_id}"
#             current_task = {
#                 'Episode': current_episode,
#                 'Task Number': task_number,
#                 'Task ID': task_key,
#                 'Descriptions': [desc],
#                 'Scores': [scores]
#             }
#             data.append(current_task)

#             if first_cell.has_attr('rowspan'):
#                 try:
#                     span = int(first_cell['rowspan'])
#                     if span > 1:
#                         rows_to_skip = span - 1
#                 except:
#                     pass
#         else:
#             if current_task is None:
#                 continue
#             desc = first_text
#             score_cells = cols[1:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             scores += [None] * (len(contestants) - len(scores))
#             current_task['Descriptions'].append(desc)
#             current_task['Scores'].append(scores)

#     # Consolidate all sub-rows
#     final_data = []
#     for task in data:
#         merged = {}
#         for i, name in enumerate(contestants):
#             all_scores = [row[i] if i < len(row) else None for row in task['Scores']]
#             cleaned_scores = []
#             for s in all_scores:
#                 if s in ('✘', '–', '-', '', None):
#                     cleaned_scores.append(0)
#                 elif s == '✔':
#                     cleaned_scores.append(1)
#                 else:
#                     try:
#                         cleaned_scores.append(int(s))
#                     except:
#                         cleaned_scores.append(0)
#             merged[name] = sum(cleaned_scores)

#         final_data.append({
#             'Episode': task['Episode'],
#             'Task Number': task['Task Number'],
#             'Task ID': task['Task ID'],
#             'Description': " ".join(task['Descriptions']).strip(),
#             **merged
#         })

#     # Fill in missing contestants (e.g. one-person task)
#     for row in final_data:
#         for name in contestants:
#             if name not in row:
#                 row[name] = 0

#     df = pd.DataFrame(final_data)
#     return df


# #def extract_taskmaster_table(table):
#     def get_clean_score(td):
#         for tag in td.find_all(['sup', 'small']):
#             tag.decompose()
#         text = td.get_text(strip=True).replace('\xa0', '')
#         return text if text != '' else None

#     def safe_int(val):
#         if val in ('✘', '–', '-', '', None):
#             return 0
#         if val == '✔':
#             return 1
#         try:
#             return int(val)
#         except:
#             return 0

#     rows = table.find_all('tr')
#     if not rows or len(rows[0].find_all('th')) < 3:
#         return pd.DataFrame()

#     header_cells = rows[0].find_all('th')
#     contestants = [th.get_text(strip=True) for th in header_cells[2:]]

#     data = []
#     current_episode = ''
#     task_id = 0
#     current_task = None
#     rows_to_skip = 0

#     def is_new_task_row(row, first_cell_text):
#         row_class = row.get('class', [])

#         # Episode or total rows are not tasks
#         if 'tmtableepisode' in row_class or 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
#             return False

#         # Accept if first cell text is alphanumeric (numbers or letters like S or T)
#         if re.match(r'^[A-Za-z0-9]+$', first_cell_text):
#             return True

#         # Or if first cell has a link
#         if row.find('a'):
#             return True

#         # As a fallback, if first cell text is non-empty and enough columns, treat as new task
#         if first_cell_text.strip() != '' and len(row.find_all(['td', 'th'])) >= 3:
#             return True

#         return False

#     for idx, row in enumerate(rows[1:], start=1):
#         row_class = row.get('class', [])
#         cols = row.find_all(['td', 'th'])
#         if len(cols) < 2:
#             print(f"[DEBUG] Skipping row {idx}: fewer than 2 columns")
#             continue

#         first_cell = cols[0]
#         first_text = first_cell.get_text(strip=True)

#         # New episode row
#         if 'tmtableepisode' in row_class:
#             current_episode = row.get_text(strip=True).split(' (')[0]
#             task_id = 0
#             current_task = None
#             rows_to_skip = 0
#             print(f"[DEBUG] New episode: {current_episode} at row {idx}")
#             continue

#         if 'tmtabletotal' in row_class or 'tmtablegrandtotal' in row_class:
#             print(f"[DEBUG] Skipping total row at {idx}")
#             continue

#         if rows_to_skip > 0:
#             is_new = False
#             rows_to_skip -= 1
#             print(f"[DEBUG] Continuation row at {idx}, rows_to_skip left: {rows_to_skip}")
#         else:
#             is_new = is_new_task_row(row, first_text)

#         if is_new:
#             task_number = first_text
#             desc = cols[1].get_text(" ", strip=True)
#             score_cells = cols[2:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             scores += [None] * (len(contestants) - len(scores))

#             task_id += 1
#             task_key = f"{current_episode.split(':')[0]}-T{task_id}"

#             current_task = {
#                 'Episode': current_episode,
#                 'Task Number': task_number,
#                 'Task ID': task_key,
#                 'Descriptions': [desc],
#                 'Scores': [scores]
#             }
#             data.append(current_task)
#             print(f"[DEBUG] New task detected: {task_key} - {task_number} at row {idx}")

#             # Rowspan handling
#             if first_cell.has_attr('rowspan'):
#                 try:
#                     span = int(first_cell['rowspan'])
#                     if span > 1:
#                         rows_to_skip = span - 1
#                         print(f"[DEBUG] Rowspan {span} detected at row {idx}")
#                 except:
#                     pass
#         else:
#             if current_task is None:
#                 print(f"[WARNING] Continuation row but no current task at row {idx}!")
#                 continue
#             desc = first_text
#             score_cells = cols[1:]
#             scores = [get_clean_score(sc) for sc in score_cells]
#             scores += [None] * (len(contestants) - len(scores))
#             current_task['Descriptions'].append(desc)
#             current_task['Scores'].append(scores)
#             print(f"[DEBUG] Continuation row for task {current_task['Task ID']} at row {idx}")

#     # Consolidate tasks
#     final_data = []
#     for task in data:
#         merged_scores = {}
#         for i, name in enumerate(contestants):
#             scores_for_contestant = [row[i] if i < len(row) else None for row in task['Scores']]
#             cleaned_scores = [safe_int(s) for s in scores_for_contestant]
#             merged_scores[name] = sum(cleaned_scores)

#         full_desc = " ".join(task['Descriptions']).strip()

#         prize_task = 1 if re.search(r'\bPrize\b', full_desc, re.I) or re.match(r'Prize', task['Task Number'], re.I) else 0
#         live_task = 1 if re.search(r'\bLive\b', full_desc, re.I) else 0
#         team_task = 1 if re.search(r'\bTeam\b', full_desc, re.I) else 0
#         tie_break = 1 if task['Task Number'] == 'T' or re.search(r'Tie Break', full_desc, re.I) else 0
#         bonus_task = 1 if (task['Task Number'].isalpha() and task['Task Number'] not in ['T']) or re.search(r'Bonus', full_desc, re.I) else 0

#         final_data.append({
#             'Episode': task['Episode'],
#             'Task Number': task['Task Number'],
#             'Task ID': task['Task ID'],
#             'Description': full_desc,
#             **merged_scores,
#             'Tasknumber': task['Task Number'],
#             'Series': current_episode.split()[0] if current_episode else '',
#             'Team Task': team_task,
#             'Prize Task': prize_task,
#             'Live Task': live_task,
#             'Tie Break': tie_break,
#             'Bonus Task': bonus_task,
#         })

#     df = pd.DataFrame(final_data)

#     # Fix columns for contestants
#     for c in contestants:
#         if c not in df.columns:
#             df[c] = 0
#         else:
#             df[c] = df[c].fillna(0).astype(int)

#     print(df.head())

#     return df
