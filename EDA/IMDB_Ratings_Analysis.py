import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

imdb_data = pd.read_csv(file_path + 'Taskmaster_IMDB_Ratings.csv')

print(imdb_data.head())


heatmap_data = imdb_data.pivot(index="Series", columns="Episode", values="Rating")
heatmap_data = heatmap_data.sort_index(ascending=False)

sns.heatmap(
    heatmap_data,
    cmap="RdYlGn",
    vmin=6, vmax=10,
    annot=True,
    fmt=".1f",
    linewidths=0.3,
    linecolor="gray",
    mask=heatmap_data.isnull(),
    cbar_kws={"label": "IMDb Rating"}
)

plt.title(f"IMDb Episode Ratings", fontsize=16, weight="bold")
plt.xlabel("Episode")
plt.ylabel("Season")

plt.tight_layout()
plt.show()


# heatmap_data = df.pivot(index="season", columns="episode", values="rating")

# # Put Season 1 at top (like typical charts)
# heatmap_data = heatmap_data.sort_index(ascending=False)

# # -----------------------------
# # 4. PLOT
# # -----------------------------
# plt.figure(figsize=(12, 8))

# sns.heatmap(
#     heatmap_data,
#     cmap="RdYlGn",          # red → yellow → green
#     vmin=6, vmax=10,        # IMDb-style scale
#     annot=True,             # show ratings
#     fmt=".1f",
#     linewidths=0.4,
#     linecolor="gray",
#     mask=heatmap_data.isnull(),  # hide missing episodes
#     cbar_kws={"label": "Rating"}
# )

# # -----------------------------
# # 5. LABELS & STYLE
# # -----------------------------
# plt.title("TV Series Episode Ratings", fontsize=16, weight="bold")
# plt.xlabel("Episode")
# plt.ylabel("Season")

# plt.tight_layout()

# # -----------------------------
# # 6. SHOW / SAVE
# # -----------------------------
# plt.show()