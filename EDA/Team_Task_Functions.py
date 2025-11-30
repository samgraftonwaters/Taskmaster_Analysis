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

def team_combinations(series_grouped = False):

    if series_grouped == True:

        combo_table = {
        "Team_A" : [[1, 5], [3, 5], [4, 5], [1, 4], [3, 4], [2, 3], [2, 5], [1, 3], [2, 4], [1, 2]],
        "Team_B" : [[2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 5], [1, 2, 5], [1, 4, 5], [1, 3, 4], [2, 4, 5], 
                    [1, 3, 5], [3, 4, 5]],
        "Series" : [[1, 10, 12], [2, 17], [3, 14, 16, 18], [4, 6], [5, 11], [7], [8, 19], [9, 13], [20], [15]],
        "Combos" : [3, 2, 4, 2, 2, 1, 2, 2, 1, 1]
        }

        team_combos = pd.DataFrame(combo_table)

        return(team_combos)

    if series_grouped == False:
        
        combo_table = {
            "Team_A" : [[1, 5], [1, 5], [1, 5], [3, 5], [3, 5], [4, 5], [4, 5], [4, 5], [4, 5], [1, 4], [1, 4],
                        [3, 4], [3, 4], [2, 3], [2, 5], [2, 5], [1, 3], [1, 3], [2, 4], [1, 2]],
            "Team_B" : [[2, 3, 4], [2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3], 
                        [1, 2, 3], [2, 3, 5], [2, 3, 5], [1, 2, 5], [1, 2, 5], [1, 4, 5], [1, 3, 4], [1, 3, 4], 
                        [2, 4, 5], [2, 4, 5], [1, 3, 5], [3, 4, 5]],
            "Series Number" : [1, 10, 12, 2, 17, 3, 14, 16, 18, 4, 6, 5, 11, 7, 8, 19, 9, 13, 20, 15],
        }

        team_combos = pd.DataFrame(combo_table).sort_values(by = 'Series Number').reset_index(drop = True)

        return(team_combos)

def team_scores_per_seat(file_path, file_name, combo_table):

    all_team_tasks = []
    team_task_totals = []
    team_tasks_series = []

    for series in range(1, 21):

        data = pd.read_excel(file_path + file_name, sheet_name = f'Series_{series}')
        
        data.rename(columns = {data.columns[2] : 'Seat 1', data.columns[3] : 'Seat 2', 
                                    data.columns[4] : 'Seat 3', data.columns[5] : 'Seat 4', 
                                    data.columns[6] : 'Seat 5'}, inplace = True)
        cols = data.columns
        seats = cols[2:7]

        team_tasks = data[data['Team Task'] == 1].reset_index(drop = True)

        team_tasks = team_tasks.drop(['Prize Task', 'Live Task', 'Tie Break', 'Solo Task'], axis = 1)
        
        all_team_tasks.append(team_tasks)
        
        ###

        team_tasks_summed = team_tasks[seats].sum(axis = 0).astype(int)

        team_tasks_summed['Series'] = f'S{series}'

        team_task_totals.append(team_tasks_summed)

        ###
        
        num_team_tasks = len(team_tasks[team_tasks['Extra Part'] != 1])

        team_tasks_series.append(num_team_tasks)

    all_team_tasks = pd.DataFrame(np.vstack(all_team_tasks), columns = ['Task Number', 'Description', 'Seat 1', 'Seat 2', 'Seat 3', 'Seat 4',
        'Seat 5', 'Tasknumber', 'Episode', 'Series', 'Team Task', 'Extra Part'])
    team_task_totals = pd.DataFrame(np.vstack(team_task_totals), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Series'])
    team_tasks_series = pd.DataFrame(np.vstack(team_tasks_series), columns = ['Number'])

    team_task_totals = pd.concat([team_task_totals, team_tasks_series, combo_table], axis = 1)

    return(team_task_totals, all_team_tasks)

def total_team_scores(team_table):

    A_total = []
    B_total = []
    for series in range(0, 20):

        a1 = team_table['Team_A'][series][0]
        a2 = team_table['Team_A'][series][1]

        b1 = team_table['Team_B'][series][0]
        b2 = team_table['Team_B'][series][1]
        b3 = team_table['Team_B'][series][2]

        a_total = team_table[f'Seat {a1}'][series] + team_table[f'Seat {a2}'][series]
        b_total = team_table[f'Seat {b1}'][series] + team_table[f'Seat {b2}'][series] + team_table[f'Seat {b3}'][series]

        A_total.append(a_total)
        B_total.append(b_total)

    team_table = pd.concat([team_table, pd.DataFrame(A_total, columns = ['Team A Total']), 
                                pd.DataFrame(B_total, columns = ['Team B Total'])], axis = 1)

    team_table['Team_A_per_person'] = round(team_table['Team A Total'] / 2, 1)
    team_table['Team_B_per_person'] = round(team_table['Team B Total'] / 3, 1)

    team_table['Team_A_per_task'] = round(team_table['Team A Total'] / team_table['Number'], 1)
    team_table['Team_B_per_task'] = round(team_table['Team B Total'] / team_table['Number'], 1)

    team_table['Team_A_per_person_task'] = round(team_table['Team_A_per_person'] / team_table['Number'], 1)
    team_table['Team_B_per_person_task'] = round(team_table['Team_B_per_person'] / team_table['Number'], 1)

    return(team_table)


def include_team_names(team_score_table, team_two_table, team_three_table):

    team_A_names = []
    team_B_names = []

    for series in range(1, 21):

        names_A = team_two_table[team_two_table['Series Number'] == series]['Name'].to_list()

        names_B = team_three_table[team_three_table['Series Number'] == series]['Name'].to_list()

        team_A_names.append([names_A])

        team_B_names.append([names_B])
    
    team_task_totals = pd.concat([team_score_table, pd.DataFrame(team_A_names, columns = ['Team A Names']).reset_index(drop = True), 
                                pd.DataFrame(team_B_names, columns = ['Team B Names']).reset_index(drop = True)], axis = 1)
    
    return(team_task_totals)


def percent_diff(score_team_A, score_team_B):
    
    diff = score_team_B - score_team_A

    frac = diff / score_team_B

    percent = abs(frac) * 100

    return(percent)

def get_best_worse_teams(team_table): 

    team_name_table = team_table.melt(id_vars='Series', value_vars=['Team A Names', 'Team B Names'], value_name='Team Names')
    team_name_table = team_name_table.rename({'variable' : 'Team'}, axis = 1)
    team_name_table['Team'] = team_name_table['Team'].str.replace('Team ', '').str.replace(' Names', '')
    
    team_person_task = team_table.melt(id_vars='Series', value_vars=['Team_A_per_person_task', 'Team_B_per_person_task'], value_name='TeamScoresPersonTask').drop('variable', axis=1)

    team_name_scores = pd.concat([team_name_table, team_person_task.drop('Series', axis = 1)], axis = 1)

    number_tasks = team_table[['Series', 'Number']]

    team_name_scores = pd.merge(team_name_scores, number_tasks, how = 'left', on = 'Series')

    team_name_scores['Team Names'] = team_name_scores['Team Names'].apply(lambda x: ', '.join(map(str, x)))

    team_name_scores = team_name_scores.sort_values(by = 'TeamScoresPersonTask', ascending = False).reset_index(drop = True)

    return(team_name_scores)

