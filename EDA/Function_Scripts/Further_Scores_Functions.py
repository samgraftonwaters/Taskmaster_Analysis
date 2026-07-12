import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def count_scores(dataframe, score : int, number_series : int):

    """
    Counts the number of times each score (1 - 5) was given for each seat in each series.

    Parameters:
    -----------
        dataframe (DataFrame): dataframe with all scores per episode and task in all series
        score (int): Number of the score value to be counted
        number_series (int): number of series to iterate over

    Returns:
    --------
        DataFrame that has the score count for each seat during all episodes of each series
    
    """

    count_score = []

    for series in range(1, number_series + 1):

        data = pd.read_excel(dataframe, sheet_name = f'Series_{series}')
        cols = data.columns
        contestents = cols[2:7]

        #Counting number of times contestnts scored a score of 1 or 5 in each task
        scores = data[data['Task Number'] != f'Series {series} Grand Total'].reset_index(drop = True)
        scores = scores[contestents]
        count_scores = scores[scores == score].count(axis = 0)
        count_score.append(count_scores)

    count = pd.DataFrame(np.vstack(count_score), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5'])

    series = []
    for i in range(number_series):
        series.append(f'S{count.index.values[i] + 1}')
    count['Series'] = series

    return(count)

def point_counts(datatable, named_table, score_column_name : str, int_per : str):

    """
    Creates a dataframe that contains the count for certain points per task for all contestents
    
    Parameters:
    -----------
        datatable (DataFrame): table with total counts of each score (e.g. 1 - 5) for each seat
        named_table (DataFrame): contestent name table
        score_column_name (str): Name of the column that contains the number of times each contestent was 
                                awarded e.g. 1 or 5 for each task. Example here could be "Number 1s Scored"
        int_per (str): defines whether the interger (number of 1s or 5s) or percentage (percent of 1s or 5s)
                        columns are included in the output table
    Returns:
    --------
        DataFrame that contains the following columns: Series, Seat, Name and Score Count    
    """
    if int_per == 'int':
        out = datatable.melt(id_vars="Series", value_vars=["Seat 1", "Seat 2", "Seat 3", 
                                                           "Seat 4", "Seat 5"],
            var_name="Seat", value_name="Score")
    
    if int_per == 'percent':
        out = datatable.melt(id_vars="Series", value_vars=["Seat 1 Percent", "Seat 2 Percent", 
                                                           "Seat 3 Percent", "Seat 4 Percent", "Seat 5 Percent"],
            var_name="Seat", value_name="Score")
        
        out['Seat'] = out['Seat'].str.replace(' Percent', '')
    
    merged_table = pd.merge(left = out, right = named_table, 
                                on = ['Series', 'Seat'], how = 'left')
    
    merged_table = merged_table.rename(columns = {'Score' : score_column_name})
    return(merged_table)


def most_least_scores(count_scores, named_table, score : int, size : str, int_per : str):

    """
    Finds the contestents with the most and least number of ones and fives per series. Function merges the 
    named table with contestents the count table in the final stage.

    Parameters:
    ----------
        count_scores (DataFrame): table with total counts of each score (e.g. 1 - 5) for each seat
        name_table (DataFrame): contestent name table
        score (int): score for a task (e.g. 1 - 5)
        size (string): filter to determine if the most or least number of each score for each seat is selected. 
                    Options are "most" for most number; "leat" for least number
        int_per (str): defines whether the interger (number of 1s or 5s) or percentage (percent of 1s or 5s)
                        columns are included in the output table
    
    Return:
    -------
        Returns a DataFrame with the most (if size = 'most') or least (if size = 'least') number of times
        each score was given for each seat per series.
    
    """

    most = []
    least = []
    
    for seat in range(1, 6):
        if int_per == 'int':
            count = count_scores[['Series', f'Seat {seat}']]
        if int_per == 'percent':
            count = count_scores[['Series', f'Seat {seat} Percent']]
            count = count.rename({f'Seat {seat} Percent' : f'Seat {seat}'}, axis = 1)

        mostcounts = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
        mostcounts['Seat'] = f'Seat {seat}'
        most.append(mostcounts)

        leastcounts = count[count[f'Seat {seat}'] == count[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
        leastcounts['Seat'] = f'Seat {seat}'
        least.append(leastcounts)

    if size.lower() == 'most':
        most = pd.DataFrame(np.vstack(most), columns = ['Series', f'Most {str(score)}s', 'Seat'])

        most = pd.merge(left = most, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values(f'Most {str(score)}s', ascending = False).reset_index(drop = True)

        most['index'] = most.index.values + 1

        return(most)
    
    if size.lower() == 'least':
        least = pd.DataFrame(np.vstack(least), columns = ['Series', f'Least {str(score)}s', 'Seat'])

        least = pd.merge(left = least, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values(f'Least {str(score)}s', ascending = False).reset_index(drop = True)

        least['index'] = least.index.values + 1

        return(least)


def high_low_ep_scores(data_table, named_table, direction : str):

    """
    Finds the contestents with the highest or lowest episode scores in each series

    Parameters:
    ----------
        data_tabe (DataFrame): table with total scores for each episode.
        name_table (DataFrame): contestent name table
        directon (str): to select if the highest or lowest episode scores are returned. Two options - "highest"
                        or "lowest".
    
    Returns:
    --------
        dataframe with either the highest or lowest episode scores per contestent in all series. 
    """

    highest_ep_scores = []
    lowest_ep_scores = []
    for seat in range(1, 6):
        seat_ep_score = data_table[['Series', 'Episode', f'Seat {seat}']]

        highest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].max(axis = 0)].reset_index(drop = True)
        highest_ep['Seat'] = f'Seat {seat}'
        highest_ep_scores.append(highest_ep)

        lowest_ep = seat_ep_score[seat_ep_score[f'Seat {seat}'] == seat_ep_score[f'Seat {seat}'].min(axis = 0)].reset_index(drop = True)
        lowest_ep['Seat'] = f'Seat {seat}'
        lowest_ep_scores.append(lowest_ep)

    if direction.lower() == 'highest':
        highest_ep_scores = pd.DataFrame(np.vstack(highest_ep_scores) , columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)
    
        highest_ep_scores = pd.merge(left = highest_ep_scores, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = False).reset_index(drop = True)

        highest_ep_scores['index'] = highest_ep_scores.index.values + 1

        return(highest_ep_scores)

    if direction.lower() == 'lowest':
        lowest_ep_scores = pd.DataFrame(np.vstack(lowest_ep_scores), columns = ['Series', 'Episodes', 'Score', 'Seat']).reset_index(drop = True)

        lowest_ep_scores = pd.merge(left = lowest_ep_scores, right = named_table, 
                                    on = ['Series', 'Seat'], how = 'left').sort_values('Score', ascending = True).reset_index(drop = True)

        lowest_ep_scores['index'] = lowest_ep_scores.index.values + 1

        return(lowest_ep_scores)


def episode_tie_scores(data_table):

    """
    Function to determine final episode scores and to account for tie breaks in each series. 
    
    Parameter:
    ---------
        data_table (DataFrame): dataframe with all scores per episode and task in all series

    Returns:
    --------
        episode_scores (DataFrame): dataframe that contains all final episode scores for each series (takes into
                                    account tie break score - e.g. +1 to winner)
        tie_break_scores (DataFrame): dataframe that contains all tie break tasks for all series
        before_tie_total (DataFrame): dataframe that contains total episode scores before tie breaks were considered

    """

    episode_scores = []
    tie_break_scores = []
    before_tie_total = []

    for series in range(1, 21):

        data = pd.read_excel(data_table, sheet_name = f'Series_{series}')

        cols = data.columns

        contestents = cols[2:9]

        episodes = data[data['Task Number'].str.contains(r'Ep', na = False)].reset_index(drop = True)

        tie_breaks = data[data['Task Number'] == 'T'].reset_index(drop = True)

        episodes = episodes[contestents]
        tie_breaks  = tie_breaks[contestents]

        episodes['Episode'] = episodes['Episode'].str.replace(" Total", "", regex=False)
        episodes = episodes.drop('Tasknumber', axis = 1).reset_index(drop = True)
        tie_breaks = tie_breaks.drop('Tasknumber', axis = 1).reset_index(drop = True)
        episodes_with_tie = episodes.copy()

        episodes[episodes.columns[0:5]] = (
        episodes.set_index("Episode")[episodes.columns[0:5]]
        .add(
            tie_breaks.set_index("Episode")[tie_breaks.columns[0:5]],
            fill_value=0
        ).values)

        episodes['Series'] = f'S{series}'
        tie_breaks['Series'] = f'S{series}'
        episodes_with_tie['Series'] = f'S{series}'

        episode_scores.append(episodes)
        tie_break_scores.append(tie_breaks)
        before_tie_total.append(episodes_with_tie)

    episode_scores = pd.DataFrame(np.vstack(episode_scores), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])
    
    before_tie_total = pd.DataFrame(np.vstack(before_tie_total), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])

    tie_break_scores = pd.DataFrame(np.vstack(tie_break_scores), columns = ['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4', 'Seat 5', 'Episode', 'Series'])

    return(episode_scores, tie_break_scores, before_tie_total)


def episodes_win_lose(episode_scores_table, named_table):

    """
    To find how many times each contestent one or lost an episode in each series

    Parameters:
    -----------
        episode_scores (DataFrame): dataframe that contains all final episode scores for each series (takes into
                                    account tie break score - e.g. +1 to winner)
        name_table (DataFrame): contestent name table
    
    Returns
    -------
        Final dataframe with each contestents number of episode wins and losses, as well as the percentages per
        number of series episodes
    """


    seat_cols = [c for c in episode_scores_table.columns if c.startswith("Seat")]

    episode_win_lose = episode_scores_table.melt(
        id_vars=["Episode", "Series"],
        value_vars=seat_cols,
        var_name="Seat",
        value_name="Score"
    )

    episode_win_lose["max_score"] = episode_win_lose.groupby(["Series", "Episode"])["Score"].transform("max")
    episode_win_lose["min_score"] = episode_win_lose.groupby(["Series", "Episode"])["Score"].transform("min")

    episode_win_lose["Win"]  = episode_win_lose["Score"] == episode_win_lose["max_score"]
    episode_win_lose["Loss"] = episode_win_lose["Score"] == episode_win_lose["min_score"]

    episode_win_lose["Number_Episodes"] = episode_win_lose.groupby("Series")["Episode"].transform("count")

    episode_win_lose_results = (
        episode_win_lose.groupby(["Series", "Seat"])
        .agg(
            Wins=("Win", "sum"),
            Losses=("Loss", "sum"),
            Number_Episodes=("Episode", "nunique")
        )
        .reset_index()
    )

    episode_win_lose_results["Series_num"] = episode_win_lose_results["Series"].str.extract(r"(\d+)").astype(int)

    episode_win_lose_results = episode_win_lose_results.sort_values("Series_num").drop(columns="Series_num")

    episode_win_lose_results = pd.merge(left = episode_win_lose_results, right = named_table,
                                        on = ['Series', 'Seat'], how = 'left')

    episode_win_lose_results['Percentage_Won'] = round((episode_win_lose_results ['Wins'] / episode_win_lose_results ['Number_Episodes']), 2)
    episode_win_lose_results['Percentage_Lost'] = round((episode_win_lose_results ['Losses'] / episode_win_lose_results ['Number_Episodes']), 2)

    return(episode_win_lose_results)
            

def tie_break_score_calcs(tie_break_scores_table, before_tie_total_table):

    """
    Calculate the scores for each tie break for all series

    Parameters:
    -----------
        tie_break_scores_table (DataFrame): dataframe with all tie breaks and number of wins/losses for each 
                                            contestent
        before_tie_total_table (DataFrame): dataframe with the episode scores before the tiebreak point is added
                                            to the winner's total

    Returns:
    ---------
        DataFrame with the tie break scores for each seat for all episodes where they occur. 
    """

    tie_break_scores = tie_break_scores_table.merge(
    before_tie_total_table,
    on=["Series", "Episode"],
    suffixes=("_tb", "_score")
    )

    seat_cols = [f"Seat {i}" for i in range(1, 6)]

    rows = []
    loser_doubles = []
    for _, row in tie_break_scores.iterrows():
        series = row["Series"]
        episode = row["Episode"]

        scores = {seat: row[f"{seat}_score"] for seat in seat_cols}
        score_counts = pd.Series(scores).value_counts()
        tied_only = score_counts[score_counts >= 1]

        if tied_only.empty:
            continue  # no tie at all

        tied_scores = [tied_only.index.max()]

        for tied_score in tied_scores:
            tied_seats = [seat for seat, tie in scores.items() if tie == tied_score]

            winners = [seat for seat in tied_seats if row[f"{seat}_tb"] == 1]
            losers  = [seat for seat in tied_seats if row[f"{seat}_tb"] == 0]
            loser_doubles.append([series, episode, losers])
  
            for win in winners:
                for lost in losers:
                    rows.append({
                        "Series": series,
                        "Episode": episode,
                        "Seat Winner": win,
                        "Seat Loser": lost})

    tie_break_scores = pd.DataFrame(rows)

    #count number of times a series has more than two losers in a tie break
    double_losers = pd.DataFrame(loser_doubles, columns = ['Series', 'Episode', 'Seat Counts'])
 
    multiple_losers = []
    for i in range(len(loser_doubles)):
        if len(double_losers['Seat Counts'][i]) >= 2:            
            losers = 1 
            multiple_losers.append(losers)
        else:
            losers = 0 
            multiple_losers.append(losers)
    
    double_losers = pd.concat([double_losers, pd.Series(multiple_losers), pd.Series(multiple_losers)], axis = 1)
    double_losers.columns = ['Series', 'Episode', 'Seat Count', 'Double Losers', 'Double Losers Series']

    double_losers_episodes = double_losers.groupby(['Series', 'Episode'])['Double Losers'].sum().reset_index()
    double_losers_series = double_losers.groupby(['Series'])['Double Losers Series'].sum().reset_index()

    tie_break_scores = pd.merge(left = tie_break_scores, right = double_losers_episodes, 
                                 on = ['Series', 'Episode'], how = 'left')
    tie_break_scores = pd.merge(left = tie_break_scores, right = double_losers_series, 
                                 on = ['Series'], how = 'left')
    
    return(tie_break_scores)

def merged_tie_scores_names(tie_break_scores, named_table):

    """
    Merge the tie break scores table with the named table to get contestent names

    Parameters:
    ----------
        tie_break_scores (DataFrame): tablt that contains the tie break scores for each seat
        named_table (DataFrame): contestent name table

    Returns:
    --------
        Merged dataframe that contains the tie break scores for each contestent who featured in a tie break
    
    """

    tie_break_scores_names = (
        tie_break_scores
        .merge(
        named_table,
            left_on=["Series", "Seat Winner"],
            right_on=["Series", "Seat"],
            how="left"
        )
        .rename(columns={"Name": "Seat Winner Name"})
        .drop(columns="Seat")
    )

    tie_break_scores_names = (
        tie_break_scores_names
        .merge(
            named_table,
            left_on=["Series", "Seat Loser"],
            right_on=["Series", "Seat"],
            how="left"
        )
        .rename(columns={"Name": "Seat Loser Name"})
        .drop(columns="Seat")
    )

    tie_break_scores_names["Tie breaks per series"] = (
        tie_break_scores_names.groupby("Series")["Episode"]
        .transform("count")
    )

    tie_break_scores_names = tie_break_scores_names[["Series", "Episode", "Seat Winner",
            "Seat Winner Name", "Seat Loser", "Seat Loser Name", 
            "Tie breaks per series", "Double Losers", "Double Losers Series"]]

    tie_break_scores_names['Tie breaks per series'] = tie_break_scores_names['Tie breaks per series'] - tie_break_scores_names['Double Losers Series']
    tie_break_scores_names = tie_break_scores_names.drop("Double Losers Series", axis = 1)
    
    return(tie_break_scores_names)


def tie_break_winners(tie_break_scores_names):

    """
    Determine who won their respective tie breaks in all series

    Parameters:
    -----------
        tie_break_scores_names (DataFrame): Merged dataframe that contains the tie break scores for each 
                                            contestent who featured in a tie break

    Returns:
    --------
        Dataframe with all winners for each tie break
    
    """

    count_names = pd.DataFrame(pd.concat([tie_break_scores_names['Seat Winner Name'], tie_break_scores_names['Seat Loser Name']], axis = 0), columns = ['Name'])
    count_names_counts = count_names.value_counts().reset_index()
    count_names_counts.columns = ["Name", "Tie Breaks per Person"]

    tie_break_count_winners = (tie_break_scores_names[["Series", "Seat Winner Name", "Seat Winner", 
                                                    "Tie breaks per series", "Double Losers"]]
        .rename(columns={"Seat Winner Name": "Name", "Seat Winner" : "Seat"})
        .assign(Wins=1)
        .groupby(["Series", "Name", "Seat", "Tie breaks per series", "Double Losers"], 
                as_index=False)["Wins"].sum())

    tie_break_count_winners = pd.merge(left = tie_break_count_winners, right = count_names_counts, on = 'Name',
                                    how = 'left')

    group_cols = ["Series", "Name", "Seat"]
    row_counts = tie_break_count_winners.groupby(group_cols).size()
    multi_row_keys = row_counts[row_counts > 1].index

    wins_multi = tie_break_count_winners.set_index(group_cols).loc[multi_row_keys].reset_index()
    wins_single = tie_break_count_winners.set_index(group_cols).drop(multi_row_keys, errors="ignore").reset_index()

    wins_multi_clean = (wins_multi.groupby(group_cols, as_index=False).agg({
            "Tie breaks per series": "max",
            "Double Losers": "sum",
            "Wins": "sum",
            "Tie Breaks per Person": "max"}))
    
    tie_break_count_winners = pd.concat([wins_single, wins_multi_clean], ignore_index=True)

    tie_break_count_winners['Tie Breaks per Person'] = tie_break_count_winners['Tie Breaks per Person'] - tie_break_count_winners['Double Losers']
    tie_break_count_winners['Wins'] = round((tie_break_count_winners["Wins"] - tie_break_count_winners["Double Losers"]),2)
    
    return(tie_break_count_winners)

def tie_break_losers(tie_break_scores_names):

    """
    Determine who lost their respective tie breaks in all series

    Parameters:
    -----------
        tie_break_scores_names (DataFrame): Merged dataframe that contains the tie break scores for each 
                                            contestent who featured in a tie break

    Returns:
    --------
        Dataframe with all losers for each tie break
    
    """

    count_names = pd.DataFrame(pd.concat([tie_break_scores_names['Seat Winner Name'], tie_break_scores_names['Seat Loser Name']], axis = 0), columns = ['Name'])
    count_names_counts = count_names.value_counts().reset_index()
    count_names_counts.columns = ["Name", "Tie Breaks per Person"]

    tie_break_count_losers = (tie_break_scores_names[["Series", "Seat Loser Name", "Seat Loser",
                                                    "Tie breaks per series", "Double Losers"]]
        .rename(columns={"Seat Loser Name": "Name", "Seat Loser" : "Seat"})
        .assign(Losses=1)
        .groupby(["Series", "Name", "Seat", "Tie breaks per series", "Double Losers"],
                as_index=False)["Losses"].sum())

    tie_break_count_losers = pd.merge(left = tie_break_count_losers, right = count_names_counts, on = 'Name',
                                    how = 'left')
    
    group_cols = ["Series", "Name", "Seat"]
    row_counts = tie_break_count_losers.groupby(group_cols).size()
    multi_row_keys = row_counts[row_counts > 1].index

    losses_multi = tie_break_count_losers.set_index(group_cols).loc[multi_row_keys].reset_index()
    losses_single = tie_break_count_losers.set_index(group_cols).drop(multi_row_keys, errors="ignore").reset_index()

    losses_multi_clean = (losses_multi.groupby(group_cols, as_index=False).agg({
            "Tie breaks per series": "max",
            "Double Losers": "sum",
            "Losses": "sum",
            "Tie Breaks per Person": "max"}))

    tie_break_count_losers = pd.concat([losses_single, losses_multi_clean], ignore_index=True)

    return(tie_break_count_losers)

def tie_break_winners_losers(tie_break_count_winners, tie_break_count_losers):

    """
    Combined table of both winners and losers for tie break tasks

    Parameters:
    -----------
        tie_break_count_winners (DataFrame): Dataframe with all winners for each tie break
        tie_break_count_losers (DataFrame): Dataframe with all losers for each tie break

    Returns:
    --------
        Combined table with all contestesnts who featured in a tie break with how many times they won or lost them
    
    """

    tie_break_count_winners_losers = (
        pd.concat([
            tie_break_count_winners.rename(columns={"Wins": "Count"}).assign(Result="Win"),
            tie_break_count_losers.rename(columns={"Losses": "Count"}).assign(Result="Loss")
        ]).sort_values(["Series", "Name"]).reset_index(drop=True))

    tie_break_count_winners_losers = tie_break_count_winners_losers.replace(np.nan, 0)

    return(tie_break_count_winners_losers)

def tie_break_counts_win_lose(tie_break_count_winners_table, tie_break_count_losers_table):

    """
    Updates the tie break winners and losers tables by calculating percentage wins/losses for each contestent.
    
    Parameters:
    -----------
        tie_break_count_winners_table (DataFrame): Dataframe with all winners for each tie break
        tie_break_count_losers_table (DataFrame): Dataframe with all losers for each tie break
    
    Returns:
    -------
        top_tie_break_count_winners (DataFrame): Updated winners dataframe with percentage wins per series or number
                                                of times each contested played a tie break task
        top_tie_break_count_losers (DataFrame): Updated winners dataframe with percentage losses per series or number
                                                of times each contested played a tie break task
    """

    tie_break_count_winners = tie_break_count_winners_table.copy()
    tie_break_count_losers = tie_break_count_losers_table.copy()

    #tie_break_count_winners['Wins'] = tie_break_count_winners['Wins'] - tie_break_count_winners['Double Losers']
    #tie_break_count_losers['Losses'] = tie_break_count_losers['Losses'] - tie_break_count_losers['Double Losers']

    tie_break_count_winners['Percentage Wins Series'] = round((tie_break_count_winners["Wins"] / tie_break_count_winners['Tie breaks per series']),2)
    tie_break_count_losers['Percentage Losses Series'] = round((tie_break_count_losers["Losses"] / tie_break_count_losers['Tie breaks per series']),2)

    tie_break_count_winners['Percentage Wins Person'] = round((tie_break_count_winners["Wins"] / tie_break_count_winners['Tie Breaks per Person']),2)
    tie_break_count_losers['Percentage Losses Person'] = round((tie_break_count_losers["Losses"] / tie_break_count_losers['Tie Breaks per Person']),2)

    top_tie_break_count_winners = tie_break_count_winners.sort_values(by = ['Percentage Wins Person', 'Wins'], ascending = False).reset_index(drop = True)
    top_tie_break_count_losers = tie_break_count_losers.sort_values(by = ['Percentage Losses Person', 'Losses'], ascending = False).reset_index(drop = True)

    return(top_tie_break_count_winners, top_tie_break_count_losers)


def tie_break_person_series_plots(data_table, win_lose : str, plot_title : str, bar_label : str,
                                  wins_lose_column : str, percent_column: str, ties_series_person_column : str,
                                  name_column : str, series_column : str, seat_column : str, n_series : int):

    """
    Plots a bar chart for the most tie break wins depending on number of tie breaks in an episode, or number for
    each contestent.

    Parameters:
    ----------
        data_table (DataFrame): dataframe with the data to plot
        win_lose (str): To set whether the plot should display the winnners ('win') or losers ('lose').
                        Options here are 'win' or 'lose' only.
        plot_title (str): Title of the plot
        bar_label (str) : label for the bar chart panel - e.g. 'Most Tie Breaks Won'
        Wins_lose_column (str): column that contains the number of wins or losses for tie breaks
        percent_column (str): column that contains the percentage of wins or losses - e.g. 'Percentage Wins Person'
        ties_series_person_column (str):å column that contains the number of series ties or ties per person -
                                        e.g. 'Tie Breaks per Person'
        name_column (str): column that contains contestent names
        series_column (str): column that contains the series numbers
        seat_column (str): column that contains each seat
        n_series (int): number of series in data table (e.g. 20)

    Returns:
    --------
        Bar chart to display percentage of wins for each contestent (in the top 20) either per number of tie breaks
        in each series or number of tie breaks for each contestent.

    """

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.05, right = 0.98)

    if win_lose.lower() == 'win':
    
        plt.barh(width=data_table[percent_column], y=data_table[name_column],
            color='red', alpha=0.8, edgecolor='white', label=bar_label)
    
    if win_lose.lower() == 'lose':

        plt.barh(width=data_table[percent_column], y=data_table[name_column],
            color='dodgerblue', alpha=0.8, edgecolor='white', label=bar_label)

    for i, (wins, percent, tie_person, name, series, seat) in enumerate(zip(data_table[wins_lose_column], 
                                                                        data_table[percent_column],
                                                data_table[ties_series_person_column],
                                                data_table[name_column],
                                                data_table[series_column],
                                                data_table[seat_column])):
        
        plt.text(-0.32, i, series, va='center', ha='left', fontsize=12, color='black')
        plt.text(-0.14, i, tie_person, va='center', ha='left', fontsize=12, color='black')
        plt.text(-0.08, i, seat, va='center', ha='left', fontsize=12, color = 'black')
        plt.text(0.05, i, name, va='center', ha='left', fontsize=12, color = 'white')
        plt.text(-0.32, 19, 'Series', fontsize = 12, color = 'black')
        plt.text(-0.17, 19, '# Ties', fontsize = 12, color = 'black')

        if win_lose.lower() == 'win':
            plt.text(-0.24, 19, 'Wins', fontsize = 12, color = 'red')
            plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='red')
            plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'red')
        if win_lose.lower() == 'lose':
            plt.text(-0.24, 19, 'Losses', fontsize = 12, color = 'blue')   
            plt.text(-0.22, i, wins, va='center', ha='left', fontsize=12, color='blue')
            plt.text(percent + 0.02, i, percent, va='center', ha='left', fontsize=12, color = 'blue')     

    plt.xlim(-0.35, 1.1)
    plt.ylim(-1, n_series)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 18)
    plt.yticks([])
    plt.ylabel('')
    plt.title(plot_title, fontsize = 22)
    plt.show()


def least_most_points(data_table_most, data_table_least, series_column : str, seat_column : str,
                      name_column : str, most_column : str, least_column : str, plot_title : str):
    
    """
    Bar chart to display the most and least number of times each person scrored a particular point for all tasks

    Parameters:
    -----------
        data_table_most (DataFrame): data table that contains the most number of counts for a certain score (e.g. most 5s)
        data_table_least (DataFrame): data table that contains the least number of counts for a certain score (e.g. least 1s)
        name_column (str): column that contains contestent names
        series_column (str): column that contains the series numbers
        seat_column (str): column that contains each seat
        most_column (str): column that contains the count for the most number of teams each point was given (e.g. most 1s)
        least_column (str): column that contains the count for the least number of teams each point was given (e.g. least 5s)
        plot_title (str): Title of the plot
    
    Returns:
    -------
        split panel bar charts to show the most and least number of times each point (e.g. 1s or 5s) was awarded
        to each contested for each task.
    
    """

    fig, (ax1, ax2) = plt.subplots(ncols = 1, nrows = 2, sharex = True)
    plt.subplots_adjust(wspace=0, hspace=0.05, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

    sns.barplot(data_table_most, x=most_column, y='index', orient="y", hue = seat_column, legend = False, ax = ax1)

    for i, (score, name, series, seat) in enumerate(zip(data_table_most[most_column], data_table_most[name_column],
                                                data_table_most[series_column], data_table_most[seat_column])):
        ax1.text(3.2, i, name, va='center', ha='left', fontsize=15, color='white')
        ax1.text(8.1, i, series, va='center', ha='left', fontsize=15, color='white')
        ax1.text(9, i, seat, va='center', ha='left', fontsize=15, color = 'white')
        ax1.text(score+0.1, i, score, fontsize = 15, color = 'black')
        
    sns.barplot(data_table_least, x=least_column, y="index", orient="y", hue = seat_column, legend = False, ax = ax2)

    for i, (score, name, series, seat) in enumerate(zip(data_table_least[least_column], data_table_least[name_column],
                                                data_table_least[series_column], data_table_least[seat_column])):
        ax2.text(5, i, name, va='center', ha='left', fontsize=15, color='black')
        ax2.text(8, i, series, va='center', ha='left', fontsize=15, color='black')
        ax2.text(9, i, seat, va='center', ha='left', fontsize=15, color = 'black')
        ax2.text(score+0.1, i, score, fontsize = 15, color = 'black')

    ax1.text(18, 4, most_column, fontsize = 20, color = 'black')
    ax2.text(18, 4, least_column, fontsize = 20, color = 'black')

    ax1.set_yticks([],[])
    ax2.set_yticks([],[])
    ax1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    ax2.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    ax2.tick_params(axis = 'x', labelsize = 14)
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    ax1.set_xlim(0, 21)
    ax2.set_xlim(0, 21)
    plt.suptitle(plot_title, fontsize = 20)
    plt.show()


def least_most_percentage(data_table_most, data_table_least, series_column : str, seat_column : str,
                      name_column : str, most_column : str, least_column : str, plot_title : str):
    
    """
    Bar chart to display the percentage of most and least times each person scrored a particular point for all tasks

    Parameters:
    -----------
        data_table_most (DataFrame): data table that contains the most number of counts for a certain score (e.g. most 5s)
        data_table_least (DataFrame): data table that contains the least number of counts for a certain score (e.g. least 1s)
        name_column (str): column that contains contestent names
        series_column (str): column that contains the series numbers
        seat_column (str): column that contains each seat
        most_column (str): column that contains the count for the most number of teams each point was given (e.g. most 1s)
        least_column (str): column that contains the count for the least number of teams each point was given (e.g. least 5s)
        plot_title (str): Title of the plot
    
    Returns:
    -------
        split panel bar charts to show the most and least times each point (e.g. 1s or 5s) was awarded
        to each contested for each task, presented as a percentage.
    
    """

    fig, (ax1, ax2) = plt.subplots(ncols = 1, nrows = 2, sharex = True)
    plt.subplots_adjust(wspace=0, hspace=0.05, bottom = 0.1, top = 0.94, left = 0.05, right = 0.96)

    sns.barplot(data_table_most, x=most_column, y='index', orient="y", hue = seat_column, legend = False, ax = ax1)

    for i, (score, name, series, seat) in enumerate(zip(data_table_most[most_column], data_table_most[name_column],
                                                data_table_most[series_column], data_table_most[seat_column])):
        ax1.text(1, i, name, va='center', ha='left', fontsize=15, color='white')
        ax1.text(10, i, series, va='center', ha='left', fontsize=15, color='white')
        ax1.text(14, i, seat, va='center', ha='left', fontsize=15, color = 'white')
        ax1.text(score+0.1, i, f'{score:.2f}', fontsize = 15, color = 'black')
        
    sns.barplot(data_table_least, x=least_column, y="index", orient="y", hue = seat_column, legend = False, ax = ax2)

    for i, (score, name, series, seat) in enumerate(zip(data_table_least[least_column], data_table_least[name_column],
                                                data_table_least[series_column], data_table_least[seat_column])):
        ax2.text(17,  i, name, va='center', ha='left', fontsize=15, color='black')
        ax2.text(26, i, series, va='center', ha='left', fontsize=15, color='black')
        ax2.text(28, i, seat, va='center', ha='left', fontsize=15, color = 'black')
        ax2.text(score+0.1, i, f'{score:.2f}', fontsize = 15, color = 'black')

    ax1.text(35, 4, 'Percentage ' + most_column, fontsize = 18, color = 'black')
    ax2.text(35, 4, 'Percentage ' + least_column, fontsize = 18, color = 'black')

    ax1.set_yticks([],[])
    ax2.set_yticks([],[])
    ax1.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax2.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax2.tick_params(axis = 'x', labelsize = 14)
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    ax1.set_xlim(0, 45)
    ax2.set_xlim(0, 45)
    ax2.set_xlabel('Percentage', fontsize = 20)
    plt.suptitle(plot_title, fontsize = 20)
    plt.show()