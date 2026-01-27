import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, kruskal
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

def gender_count_percent(gender_age_table):
    """
    Measures the percentage of male, female and non-binary contestents in all series.

    Parameters:
    -----------
        gender_age_table (DataFrame): table that contains each contestent's age range and gender, along with
        searies, seat, name, etc.

    Returns:
    ---------
        table with value counts and percentages of gender for all contestents
    
    """
    gender_count = gender_age_table['Gender'].value_counts().reset_index()
    gender_count.columns = ['Gender', 'Count']
    gender_count['Percent'] = (gender_count['Count'] / gender_count['Count'].sum() ) * 100
    print(gender_count)
    return(gender_count)

def gender_count_series(gender_age_table):
    """
    counts the number of male, female and non-binary contestents for each series separately

    Parameters:
    -----------
        gender_age_table (DataFrame): table that contains each contestent's age range and gender, along with
                                        searies, seat, name, etc.

    Returns:
    ---------
        table with value counts of gender for all contestents in each series
    
    """
    gender_series = gender_age_table.groupby('Series Number')['Gender'].value_counts().reset_index()
    gender_series = gender_series.sort_values('Series Number', ascending = True)
    print(gender_series)
    return(gender_series)


def gender_count_series_bar(gender_age_table, series_seat : bool, title: str):
    """
    Creates a bar chart for the number of male, female or non-binary contestests either per series or for each seat

    Parameters:
    ----------
        gender_age_table (DataFrame): table that contains each contestent's age range and gender, along with
                                        searies, seat, name, etc.
        series_seat (boolean): if 'seat', then the count for all seats of each gender is plotted, if 'series'
                                then the count of all genders from each series is plotted
        title (str): title of the plot
    
    Returns:
    --------
        Bar chart to show number of contestents' gender based either on series or seat.
    """

    if series_seat.lower() == 'series':
        gender_series_plot = gender_age_table.groupby(['Series Number', 'Gender']).size().unstack(fill_value=0)
        series = gender_series_plot.index
        x = np.arange(len(series))+1
        x_label = 'Series'
        x_range = (0.25, 20.75)
        y_range = (0, 5)
    
    if series_seat.lower() == 'seat':
        gender_series_plot = gender_age_table.groupby(['Seat', 'Gender']).size().unstack(fill_value=0)
        seat = gender_series_plot.index
        x = np.arange(len(seat))+1
        x_label = 'Seat'
        x_range = (0.5, 5.5)
        y_range = (0, 15)

    width = 0.4

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)
    
    # Plot Male and Female bars side by side
    plt.bar(x - width/2, gender_series_plot['Male'], width, label='Male', color='dodgerblue', alpha = 0.8,
            edgecolor = 'black')
    plt.bar(x + width/2, gender_series_plot['Female'], width, label='Female', color='green', alpha = 0.8,
            edgecolor = 'black')
    plt.scatter(x[gender_series_plot['Non-Binary'] == 1], 
               gender_series_plot.loc[gender_series_plot['Non-Binary'] == 1, 'Non-Binary'],
               color='red', marker='D', s=100, label='Non-Binary')
    
    for i in range(len(gender_series_plot)):
        i = i + 1
        plt.text(i - 0.2, gender_series_plot['Male'][i] + 0.25, gender_series_plot['Male'][i], ha='center', fontsize=16, color='blue')
        plt.text(i + 0.2, gender_series_plot['Female'][i] + 0.25, gender_series_plot['Female'][i], ha='center', fontsize=16, color='green')

    plt.xlabel(x_label, fontsize = 20)
    plt.ylabel('Count', fontsize = 20)
    plt.ylim(y_range)
    plt.xlim(x_range)
    plt.title(title, fontsize = 25)
    plt.xticks(x, fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.legend(fontsize = 18)
    plt.show()

def setting_age_bins(table):
    """
    creates age bins based on each contestents ages.

    Parameters:
    ----------
        table (DataFrame): data table that contains series, contestent names, and ages
    
    Returns:
    -------
        input datatable with an extra column containing the age bins
    
    """
    age_table = table.copy()
    age_bins = [20, 30, 40, 50, 60, 70]
    age_labels = ['20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69']
    age_table['Age_Ranges'] = pd.cut(age_table['Age_at_First_Air'], bins = age_bins, labels = age_labels, right = False)
    print(age_table)
    return(age_table)

def age_range_metrics(table):
    """
    counts the age ranges and measures corresponding perentage for each age range for all contestents
    
    Parameters:
    ----------
        table (DataFrame): data table that contains series, contestent names, ages, and age ranges (bins)
    
    Returns:
    --------
        dataframe with counts and percentage for each age range
    
    """
    age_table = table.copy()
    age_ranges_count = age_table['Age_Ranges'].value_counts().reset_index()
    age_ranges_count.columns = ['Age_Ranges', 'Count']
    age_ranges_count['Percentage'] = (age_ranges_count['Count'] / age_ranges_count['Count'].sum()) * 100
    print(age_ranges_count)
    return(age_ranges_count)

def age_group_series(table):
    """
    counts the number age ranges for each series separately

    Parameters:
    -----------
        table (DataFrame): data table that contains series, contestent names, ages, and age range bins

    Returns:
    ---------
        table with value counts of age ranges for all contestents in each series
    """
    age_table = table.copy()
    age_series = age_table.groupby('Series Number')['Age_Ranges'].value_counts().reset_index()
    age_series = age_series.sort_values('Series Number', ascending = True)
    print(age_series)
    return(age_series)

def age_series_stacked_bar(table, series_seat, title):
    """
    Creates a bar chart for the number of each each range either per series or for each seat

    Parameters:
    ----------
        table (DataFrame): table that contains each contestent's age range along with
                                        searies, seat, name, etc.
        series_seat (boolean): if 'seat', then the count for all seats of each gender is plotted, if 'series'
                                then the count of all genders from each series is plotted
        title (str): title of the plot
    
    Returns:
    --------
        Stacked bar chart to show number of contestents' age ranges based either on series or seat.
    """

    if series_seat.lower() == 'series':
        x_axis = "Series Number"
        x_label = "Series"
        text_loc_x = 0.05
        text_loc_y = 5.33
        y_ticks = [0, 1, 2, 3, 4, 5]
    
    if series_seat.lower() == 'seat':
        x_axis = "Seat"
        x_label = 'Seat'
        text_loc_x = -0.5
        text_loc_y = 21.4
        y_ticks = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    age_series_plot = table.pivot_table(index=x_axis, columns="Age_Ranges", values="count",
                aggfunc="sum", fill_value=0, observed=True).reset_index()
    
    print(age_series_plot)
    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.88, left = 0.08, right = 0.96) 
    ax = age_series_plot.plot(x=x_axis, kind='bar', stacked=True, width = 0.8, ax = ax)

    for c in ax.containers:
        labels = [f"{int(v.get_height())}"
                if np.isfinite(v.get_height()) and v.get_height() > 0 else '' for v in c]
        
        ax.bar_label(c, labels=labels, label_type='center', color = 'white', fontsize = 14)
    
    plt.text(text_loc_x, text_loc_y, 'Age Ranges:', fontsize = 14)

    ax.tick_params(axis='x', labelrotation=0)
    plt.xlabel(x_label, fontsize = 20)
    plt.ylabel("Count", fontsize = 20)
    plt.xticks(fontsize = 18)
    plt.yticks(y_ticks, fontsize = 18)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=5, fontsize=14, frameon=False)
    plt.title(title, pad=30, fontsize = 24)
    plt.show()


def merge_series_age_gender(series_table, gender_table, age_table):

    """
    Merge the series score table with the gender and age tables.

    Parameters:
    ----------
        series_table (DataFrame): table with the final series scores
        gender_table (DataFrame): table with the gender columns
        age_table (DataFrame): table with the age range columns

    Returns:
    --------
        merged dataframe with series scores, age ranges and genders.    
    """

    series_table = series_table.copy()
    gender_table = gender_table.copy() 
    age_table = age_table.copy()

    final_scores_age_gender = pd.merge(left = series_table, right = gender_table.drop('Series', axis = 1),
                                    on = 'Name', how = 'left')

    final_scores_age_gender = pd.merge(left = final_scores_age_gender, 
                                    right = age_table.drop(['Series Number', 'Age_at_First_Air'], axis = 1), 
                                    on = 'Name', how = 'left')

    print(final_scores_age_gender)
    return(final_scores_age_gender)

def seat_gender_metrics(datatable):
    """
    counts the number male, femails and non-binary contestents for each seat separately

    Parameters:
    -----------
        table (DataFrame): merged series, age groups and gender table

    Returns:
    ---------
        table with value counts of genders for all contestents in each seat
    """
    datatable = datatable.copy()
    seat_gender_table = datatable[['Seat', 'Gender']]
    seat_gender_table['Seat'] = seat_gender_table['Seat'].str.replace('Seat ', '').astype(int)
    print(seat_gender_table)
    return(seat_gender_table)

def seat_age_metrics(datatable):
    """
    counts the number age ranges for each seat separately

    Parameters:
    -----------
        table (DataFrame): merged series, age groups and gender table

    Returns:
    ---------
        table with value counts of age ranges for all contestents in each seat
    """
    datatable = datatable.copy()
    seat_age_table = datatable[['Seat', 'Age_Ranges']]
    seat_age_table['Seat'] = seat_age_table['Seat'].str.replace('Seat ', '').astype(int)
    seat_age_table = seat_age_table.groupby('Seat')['Age_Ranges'].value_counts().reset_index()
    print(seat_age_table)
    return(seat_age_table)


def chi2_test(data_table, series_episode : str, values : str, index : str, columns : str, agg : str = 'sum'):

    """
    Creates a contigency table to carry out a chi-squared test on the data

    Parameters:
    -----------
        data_table (DataFrame):  merged series, age groups and gender table
        series_episode (str): determine if series or episode tables are being used. options "series" or "episode"
        values (str): value column for the contingency table (e.g. Score). If series_episode == 'episode', set to None
        index (str): independent variable to test with (e.g. age_range or gender). If series_episode == 'episode', set to None
        columns (str): dependent variable to test against (e.g. Position). If series_episode == 'episode', set to None
        agg (str): method for the contingency table values. default = 'sum'.

    Returns:
    --------
        Prints out the observed and expected tables and summary of the Chi-Squared test
    
    """
    if series_episode.lower() == 'series':
        contingency = pd.pivot_table(data_table, values=values, index=index, columns=columns, 
                                    aggfunc=agg, fill_value=0)
    
    if series_episode.lower() == 'episode':
        contingency = data_table
    
    chi2, pvalue, dof, expected = chi2_contingency(contingency)

    expected_table = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)

    print('Observed Table:\n', contingency)
    print()
    print('Expected Table:\n', expected_table)

    print(f"Chi-squared statistic: {chi2:.3f}")
    print(f"Degrees of freedom: {dof}")
    print(f"P-value: {pvalue:.6f}")
    
    print('/n/n')


def formatting_table(data_table):

    """
    Creates additional columns to the merged score-gender-age table for bias testing 
    
    Parameters:
    -----------
        table (DataFrame): merged series, age groups and gender table
    
    Returns:
    --------
        finalised datatable with additional columns for further analysis.
    """
    df = data_table.copy()

    df['Gender'] = df['Gender'].astype('category')

    df['Age_Ranges'] = df['Age_Ranges'].astype('category')

    df['age_c'] = df['Age_at_First_Air'] - df['Age_at_First_Air'].mean()

    df['Score_Z'] = (
        df.groupby('Series')['Score']
        .transform(lambda x: (x - x.mean()) / x.std())
    )
    print(df.columns)
    return(df)

def model_fitting(data_table, target_variable : str, test_variables : list | str):

    """
    Fit the OLS model to test for bias:

    Model uses the calculated Z-score values per series (see previous function) and determines whether either
    age range or gender affects the overall perfomance (e.g. final scores). OLS (Ordinary Least Squares) 
    tests whether these factors (gender or age rage) systematically predict performance across all contestants.    
    The coefficients state the average effect of gender or age group after controlling for series.

    If a coefficient is significantly different from zero, that factor is associated with higher/lower 
    performance. So if there were systematic gender or age bias in judging or task design, we’d expect 
    the model coeffients to be significant.

    Parameters:
    -----------
        data_table (data_table): merged series, age groups and gender table
        target_variable (str): name of the column that contains the target variable (e.g. Z-score values)
        test_variables (list or str): name of the columns that you are testing bias for (e.g. gender and age range)
    
    Returns:
    --------
        Prints summary of the OLS table to be used to dertermine whether there is bias
        best fir model to be used in an ANOVA test (see next function)
    """
    df = data_table.copy()
    model = smf.ols(
        f"{target_variable} ~ {test_variables[0]} + {test_variables[1]}",
        data=df
    ).fit()

    print(f"\n=== OLS Regression: {test_variables[0]} + {test_variables[1]} ===\n")
    print(model.summary())
    return(model)

def anova_test(model):

    """
    Runs an ANOVA test on the model from the previous function

    Parameters:
    ----------
        model (model): the best fit OLS model from the previous function

    Returns:
    --------
        Prints the summary of the ANOVA Test
    """
    anova_results = anova_lm(model, typ=2)
    print("\n=== ANOVA Test ===\n")
    print(anova_results)
