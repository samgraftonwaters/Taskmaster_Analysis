import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import Team_Task_Functions as TTF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

team_table = TTF.formatting_team_table(dataframe = team_table)

print(team_table.head())

team_two = team_table[team_table['Team'] == 'A']
team_three = team_table[team_table['Team'] == 'B']



plt.figure(figsize=(10, 6))

# Map team to colors
team_colors = {"A": "dodgerblue", "B": "orange"}

# Plot points
for _, row in team_table.iterrows():
    plt.scatter(
        int(row["Seat Number"]),
        row["Series"],
        color=team_colors[row["Team"]],
        s=200,
        edgecolors="black"
    )
    # Add the name as text next to the point
    plt.text(
        int(row["Seat Number"]) + 0.05,
        row["Series"],
        row["Name"],
        va="center",
        fontsize=9
    )

plt.xlabel("Seat Number")
plt.ylabel("Series")
plt.title("Contestants by Seat and Series")
plt.xticks(sorted(team_table["Seat Number"].astype(int).unique()))
plt.grid(True, linestyle="--", alpha=0.4)

# Legend
for team, color in team_colors.items():
    plt.scatter([], [], color=color, label=f"Team {team}", s=200, edgecolors="black")

plt.legend(title="Team")
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

team_colors = {"A": "dodgerblue", "B": "orange"}

plt.figure(figsize=(10, 6))

for _, row in team_table.iterrows():
    x = int(row["Seat Number"])
    y = row["Series"]

    # Draw faint point for position (can remove if unwanted)
    plt.scatter(x, y, color="white", s=100)

    # Colour the name instead of the dot
    plt.text(
        x + 0.05,
        y,
        row["Name"],
        color=team_colors[row["Team"]],
        fontsize=10,
        va="center",
        fontweight="bold"
    )

plt.xlabel("Seat Number")
plt.ylabel("Series")
plt.title("Contestants by Seat and Series")

plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()



# Convert Series -> numeric values for plotting
team_table["Series"] = team_table["Series"].str.extract(r"(\d+)").astype(int)

team_colors = {"A": "dodgerblue", "B": "orange"}

plt.figure(figsize=(10, 6))

for _, row in team_table.iterrows():
    x = int(row["Seat Number"])
    y = row["Series"]   # ← numeric y value

    plt.text(
        x,
        y,
        row["Name"],
        ha="center",
        va="center",
        fontsize=9,
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.3",
            fc=team_colors[row["Team"]],
            ec="black",
            lw=0.7,
            alpha=0.9,
        )
    )

plt.xlabel("Seat Number")
plt.ylabel("Series")
plt.title("Contestants by Seat and Series")

# Use numeric ticks but label them with S1, S2, ...
unique_nums = sorted(team_table["Series"].unique())
plt.yticks(unique_nums, [f"S{num}" for num in unique_nums])

plt.xticks(sorted(team_table["Seat Number"].astype(int).unique()))

plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

