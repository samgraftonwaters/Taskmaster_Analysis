import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def formatting_team_table(dataframe):
    long_team_table = dataframe.melt(id_vars=["Series"], var_name="Column", value_name="Value")

    # Seat number from the end of the column name
    long_team_table["Seat Number"] = long_team_table["Column"].str.extract(r"(\d+)$")

    # Determine whether it's a Name or Team column
    long_team_table["Type"] = long_team_table["Column"].str.startswith("Seat").map({True: "Name", False: "Team"})


    # Pivot so each seat has one Name and one Team
    final_team_table = long_team_table.pivot_table(index=["Series", "Seat Number"], columns="Type",
                                                values="Value",aggfunc="first").reset_index().rename_axis(None, axis=1)

    final_team_table["Series Number"] = final_team_table["Series"].str.extract(r"(\d+)").astype(int)
    final_team_table = final_team_table.sort_values(["Series Number", "Seat Number"]).reset_index(drop = True)

    # Arrange order
    final_team_table = final_team_table[["Name", "Team", "Seat Number", "Series", "Series Number"]]

    return(final_team_table)


def plot_teams(dataframe):
    team_colors = {"A": "#3A0CA3", "B": "#004400"}

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    for _, row in dataframe.iterrows():
        x = int(row["Seat Number"])
        y = row["Series Number"]

        plt.text(x,  y,  row["Name"],  ha="center", va="center", fontsize=9, color="white",
                bbox=dict( 
                boxstyle="round,pad=0.3",
                fc=team_colors[row["Team"]],
                ec="black",
                lw=0.7,
                alpha=0.9,
            )
        )

    plt.xlabel("Seat Number", fontsize = 16)
    plt.ylabel("Series", fontsize = 20)
    plt.title("Teams for Each Series", fontsize = 18)

    # Use numeric ticks but label them with S1, S2, ...
    unique_nums = sorted(dataframe["Series Number"].unique())
    plt.yticks(unique_nums, [f"S{num}" for num in unique_nums], fontsize = 13)

    plt.xticks(sorted(dataframe["Seat Number"].astype(int).unique()), fontsize = 14)
    plt.xlim(0.5, 5.5)
    plt.ylim(0, 21)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()