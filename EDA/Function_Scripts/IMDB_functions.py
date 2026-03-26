import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(data, x_label : str, y_label : str, title : str, min_range : float | int, 
                 max_range : float | int, colourbar_label : str, decimal_places : int = 1):

    """
    Plots heatmap of IMDB ratings or similar for Taskmaster series and episodes

    Parameters:
    -----------
        data: pivot data table of series (index), episodes (columns), and heatmap values
        x_label (str): name for the x-axis
        y_label (str): name for the y-axis
        title (str): title of plot
        min_range (float | int): minimum value for the colourbar
        max_range (float | int): maximum value for the colourbar
        colourbar_label (str): label for the colourbar
        decimal_places (int): value for the number of decimal places to be displayed. default = 1
    
    Returns:
    --------
        Heatmap plot related to IMDB ratings.    
    """
    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.05, right = 0.95)
    sns.heatmap(data, vmin=min_range, vmax=max_range, annot=True,  fmt=f".{decimal_places}f", 
                linewidths=0.3, linecolor="darkgrey", mask=data.isnull(), cmap= "RdYlGn", 
                cbar_kws={"label": colourbar_label}, annot_kws={"size": 14})

    plt.title(title, fontsize=18)
    plt.xlabel(x_label, fontsize = 16)
    plt.ylabel(y_label, fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.tight_layout()
    plt.show()


def plot_linegraph_or_barchart(x_data, y_data, line_colour:str, x_label:str, y_label:str, 
                               title:str, bar_or_line : str):

    """
    Plots a line graph

    Parameters:
    -----------
        x_data: data for x-axis
        y_data: data for y-axis
        linecolour (str): colour for the line chart
        x_label (str): name for the x-axis
        y_label (str): name for the y-axis
        title (str): title of plot
        bar_or_line (str): 'bar' or 'line' options only - determines what is being plotted.
    
    Returns:
    --------
        line plot or bar chart with y-axis data average as a dashed line
    """

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.95)
    
    plt.hlines(y_data.mean(), 0.5, 20.5, lw = 4 ,linestyles='dashed', color = 'black', 
               label = f'Overall Average = {round(y_data.mean(), 2)}')

    if bar_or_line.lower() == 'bar':
        plt.bar(x=x_data, height=y_data, color = line_colour)

        for x, y in zip(x_data, y_data):
            plt.text(x, y+5, f"{y:.1f}", fontsize=12, ha='center', color = line_colour)

    if bar_or_line.lower() == 'line':
        plt.plot(x_data, y_data, '-o', markersize = 35, lw = 3, color = line_colour)

        for x, y in zip(x_data, y_data):
            plt.text(x, y-0.01, f"{y:.2f}", fontsize=12, ha='center', color = 'black')
        
    plt.xlabel(x_label, fontsize = 18)
    plt.ylabel(y_label, fontsize = 18)
    plt.title(title, fontsize = 22)
    plt.xticks(range(1, 21), fontsize = 16)
    plt.xlim(0.4, 20.6)
    plt.yticks(fontsize = 16)
    plt.legend(loc = 'best', fontsize = 18)
    plt.show()


def line_plot_episodes_series(episode_x, episode_y, series_x, series_y, series_boundaries, 
                              series_number_col, x_label : str, y_label : str, title : str):
    
    """
    Plots a line graph with two lines - one for all episodes and the other for the series average
    
    Parameters:
    -----------
        episode_x: values for x-axis in relation to the episodes data
        episode_y: values for y-axis in relation to the episodes data
        series_x: values for x-axis in relation to the averaged series data
        series_y: values for y-axis in relation to the averaged series data
        series_number_col: column containing the series numbers
        x_label (str): name for the x-axis
        y_label (str): name for the y-axis
        title (str): title of plot

    Returns:
    --------
        Plot with comparitive lines to show how the y axis changed over each series and 
        between episodes
    """

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.08, right = 0.95)

    plt.plot(range(1, len(episode_x)+1), episode_y, '-o', color = 'dodgerblue', 
            markersize = 10, lw = 3, label = 'Episodes')
    plt.plot(series_x, series_y, '-o', color = 'blueviolet',
            markersize = 14, lw = 5, label = 'Average per Series')
    plt.vlines(series_boundaries, episode_y.min() - 0.05*episode_y.max(), 
               episode_y.max() + 0.05*episode_y.max(), color = 'darkgrey', 
               linestyles='dashed', lw = 3)

    for x, series in zip(series_x, series_number_col):
        plt.text(x-1.5, episode_y.max() - 0.05*episode_y.max(), f"S{series}", fontsize = 14)

    plt.xlim(0, len(episode_x)+ 1)
    plt.ylim(episode_y.min() - 0.05*episode_y.max(), episode_y.max() + 0.05*episode_y.max())
    plt.xlabel(x_label, fontsize = 18)
    plt.ylabel(y_label, fontsize = 18)
    plt.title(title, fontsize = 22)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.legend(loc = 'best', fontsize = 18)
    plt.show()