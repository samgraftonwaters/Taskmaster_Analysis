import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver #pip install webdriver-manager
import seaborn as sns
import time
import scraping_functions as SF

# -----------------------------
# CONFIG
# -----------------------------
SHOW_ID = "tt4934214"  # Dexter (change this!)
MAX_SEASONS = 20       # safety cap

HEADERS = {"Content-Type": "application/json", "User-agent":"Mozilla/5.0"}

url = url = f'https://www.imdb.com/title/tt4934214/episodes/?season=1&ref_=ttep'

if SF.scrape_with_requests(url, headers = HEADERS) == 'error':
    soup = SF.scrape_with_selenium(url)
    print('scrape with selenium')
else:
    soup = SF.scrape_with_requests(url, headers = HEADERS)
    print('scrape with requests')
    

print(soup.prettify())
soup_output = soup.prettify()

with open('IMDB_Season1_Output.txt', 'w') as f:
     f.write(soup_output)

# -----------------------------
# FETCH EPISODE DATA
# -----------------------------
# all_data = []

# for season in range(1, MAX_SEASONS + 1):
#     # url = f"https://www.imdb.com/title/{SHOW_ID}/episodes?season={season}&ref_=ttep"
#     url = f'https://www.imdb.com/title/tt4934214/episodes/?season={season}&ref_=ttep'
#     print(f"Fetching season {season}...")

#     if SF.scrape_with_requests(url, headers = HEADERS) == 'error':
#         soup = SF.scrape_with_selenium(url)
#         print('scrape with selenium')
#     else:
#         soup = SF.scrape_with_requests(url, headers = HEADERS)
#         print('scrape with requests')

#     print(soup.prettify())

#     episodes = soup.find_all("div", class_="ipc-title__text")
#     ratings = soup.find_all("span", class_="ipc-rating-star--rating")

#     print(episodes)
#     print(ratings)

#     # If no episodes found → stop
#     if len(episodes) == 0:
#         break

#     ep_num = 1
#     rating_idx = 0

#     for block in soup.select(".ipc-metadata-list-summary-item"):
#         try:
#             # Extract rating
#             rating_tag = block.select_one(".ipc-rating-star--rating")
#             if rating_tag:
#                 rating = float(rating_tag.text.strip())
#             else:
#                 rating = None

#             all_data.append({
#                 "season": season,
#                 "episode": ep_num,
#                 "rating": rating
#             })

#             ep_num += 1

#         except Exception:
#             continue

#     time.sleep(1)  # be polite to IMDb

# # -----------------------------
# # DATAFRAME
# # -----------------------------
# df = pd.DataFrame(all_data)

# if df.empty:
#     raise ValueError("No data found. Check SHOW_ID.")

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

