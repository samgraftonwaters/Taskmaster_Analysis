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