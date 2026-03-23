import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver #pip install webdriver-manager
import seaborn as sns
import time
import scraping_functions as SF
import re

num_series = 20

header = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

all_data = []

for series in range(1, num_series+1):
    url = f'https://www.imdb.com/title/tt4934214/episodes/?season={series}&ref_=ttep'
    print(f"Fetching season {series}...")

    result = SF.scrape_with_requests(url, headers=header)

    if result == 'error':
        soup = SF.scrape_with_selenium_imdb(url)
        print('scrape with selenium')
    else:
        soup = result
        print('scrape with requests')

    episodes = soup.find_all("div", class_="ipc-title__text")
    ratings = soup.find_all("span", class_="ipc-rating-star--rating")
    votes = soup.find_all("span", class_="ipc-rating-star--voteCount")

    for i in range(len(episodes)):
        
        # Episode title
        title = episodes[i].text.strip()
        
        # Rating
        if i < len(ratings):
            rating = float(ratings[i].text.strip())
        else:
            None
        
        # Votes
        if i < len(votes):
            votes_text = votes[i].text
            vote_count = int(re.sub(r"[^\d]", "", votes_text))
        else:
            vote_count = None

        all_data.append({
            "Series": series,
            "Episode": i + 1,
            "Title": title,
            "Tating": rating,
            "Votes": vote_count
        })

    time.sleep(5)

df = pd.DataFrame(all_data)

print(df)

# # -----------------------------
# # PIVOT
# # -----------------------------
# heatmap_data = df.pivot(index="season", columns="episode", values="rating")
# heatmap_data = heatmap_data.sort_index(ascending=False)

# # -----------------------------
# # PLOT
# # -----------------------------
# plt.figure(figsize=(14, 8))

# sns.heatmap(
#     heatmap_data,
#     cmap="RdYlGn",
#     vmin=6, vmax=10,
#     annot=True,
#     fmt=".1f",
#     linewidths=0.3,
#     linecolor="gray",
#     mask=heatmap_data.isnull(),
#     cbar_kws={"label": "IMDb Rating"}
# )

# plt.title(f"IMDb Episode Ratings ({SHOW_ID})", fontsize=16, weight="bold")
# plt.xlabel("Episode")
# plt.ylabel("Season")

# plt.tight_layout()
# plt.show()

