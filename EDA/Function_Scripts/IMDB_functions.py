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