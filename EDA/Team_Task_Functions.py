import pandas as pd
import numpy as np

def formatting_team_table(dataframe):
    long_team_table = dataframe.melt(id_vars=["Series"], var_name="Column", value_name="Value")

    # Seat number from the end of the column name
    long_team_table["Seat Number"] = long_team_table["Column"].str.extract(r"(\d+)$")

    # Determine whether it's a Name or Team column
    long_team_table["Type"] = long_team_table["Column"].str.startswith("Seat").map({True: "Name", False: "Team"})


    # Pivot so each seat has one Name and one Team
    final_team_table = long_team_table.pivot_table(index=["Series", "Seat Number"], columns="Type",
                                                values="Value",aggfunc="first").reset_index().rename_axis(None, axis=1)

    final_team_table["Series_num"] = final_team_table["Series"].str.extract(r"(\d+)").astype(int)
    final_team_table = final_team_table.sort_values(["Series_num", "Seat Number"]).drop(columns="Series_num").reset_index(drop = True)

    # Arrange order
    final_team_table = final_team_table[["Name", "Team", "Seat Number", "Series"]]

    return(final_team_table)

