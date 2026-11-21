import time
import pandas as pd
import scraping_functions as SF

single_series_number = 21
start_series = 1
final_series = 21
output_filename_all = 'Taskmaster_Series_Scores'
output_filename_single = 'Taskmaster_Series_21_Only_Scores'

output_filepath = '../Data/'

SF.get_main_series_data_scraped(output_filepath, output_filename = output_filename_all, start_series_number = final_series,
                                 final_series_number = final_series, single_series_number = None)

SF.get_main_series_data_scraped(output_filepath, output_filename = output_filename_single, start_series_number = 21,
                                 final_series_number = 21, single_series_number = 21)
        
#Champion of Champions
champ_of_champs = ['', '_2', "_3", "_4"]
with pd.ExcelWriter(output_filepath + 'Taskmaster_CoC_Scores.xlsx') as writer:
    
    for series in champ_of_champs:

        url = f"https://taskmaster.fandom.com/wiki/Champion_of_Champions{series}"

        result = SF.scrape_with_requests(url)

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

result = SF.scrape_with_requests(url)

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
