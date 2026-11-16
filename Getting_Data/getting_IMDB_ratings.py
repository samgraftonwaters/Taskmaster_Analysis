import pandas as pd
import seaborn as sns
import time
import scraping_functions as SF
import re

output_filepath = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

num_series = 20

all_data = []

for series in range(1, num_series+1):
    url = f'https://www.imdb.com/title/tt4934214/episodes/?season={series}&ref_=ttep'
    print(f"Fetching season {series}...")

    result = SF.scrape_with_requests(url)

    if result == 'error':
        soup = SF.scrape_with_selenium_imdb(url)
        print('scrape with selenium')
    else:
        soup = result
        print('scrape with requests')

    episodes = soup.find_all("div", class_="ipc-title__text")
    ratings = soup.find_all("span", class_="ipc-rating-star--rating")
    votes = soup.find_all("span", class_="ipc-rating-star--voteCount")

    if len(ratings) > len(episodes):
        diff = len(ratings) - len(episodes)
        ratings = ratings[diff:] 

    if len(votes) > len(episodes):
        votes = votes[:len(episodes)]

    for i in range(len(episodes)):
        
        # Episode title
        title = episodes[i].text.strip()
        
        # Rating
        if i < len(ratings):
            rating = float(ratings[i].text.strip())
        else:
            rating = None

        # Votes
        if i < len(votes):
            votes_text = votes[i].text
            vote_count = int(re.sub(r"[^\d]", "", votes_text))
        else:
            vote_count = None

        all_data.append({
            "Series": series,
            "Episode": i + 1,
            "Rating": rating,
            "Votes": vote_count
        })

    time.sleep(5)

df = pd.DataFrame(all_data)

print(df)

df.to_csv(output_filepath + 'Taskmaster_IMDB_Ratings.csv', sep = ',', index = False)