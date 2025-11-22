import pandas as pd
import numpy as np

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

team_table = pd.read_csv(file_path+'Teams.csv')

print(team_table.head())


# Melt
long = team_table.melt(
    id_vars=["Series"],
    var_name="Column",
    value_name="Value"
)

print(long.head())
# Seat number from the end of the column name
long["Seat Number"] = long["Column"].str.extract(r"(\d+)$")

# Determine whether it's a Name or Team column
long["Type"] = long["Column"].str.startswith("Seat").map({True: "Name", False: "Team"})

print(long.head(30))

# Pivot so each seat has one Name and one Team
final = (
    long.pivot_table(
        index=["Series", "Seat Number"],
        columns="Type",
        values="Value",
        aggfunc="first"
    )
    .reset_index()
    .rename_axis(None, axis=1)
)

final["Series_num"] = final["Series"].str.extract(r"(\d+)").astype(int)
final = final.sort_values(["Series_num", "Seat Number"]).drop(columns="Series_num").reset_index(drop = True)

# Arrange order
final = final[["Name", "Team", "Seat Number", "Series"]]

print(final.head(30))
