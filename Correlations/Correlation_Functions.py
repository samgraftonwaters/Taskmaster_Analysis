import pandas as pd
import numpy as np
from scipy import stats
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
import seaborn as sns

def normal_variables(data_table):
    """
    determines which variables in the full contestent datatable are normally distributed or not.
    Takes the p-value to be less than 0.01 to be defined as non-normal

    Parameters:
    ----------
        data_table (DataFrame): full contestent data table (with numerical values)
    
    Returns:
        normal and non-normal Dataframes. This file also saves the tables as csv files. 
    
    """
    columns = data_table.columns

    non_normal = []
    normal = []

    for cols in columns:
        norm = stats.normaltest(data_table[cols])
        if norm.pvalue < 0.01:
            non_normal.append([cols, norm.pvalue])
            print(f'{cols} p-value = {norm.pvalue}')
        else:
            normal.append([cols, norm.pvalue])
            print(f'{cols} p-value = {norm.pvalue}')

    non_normal = pd.DataFrame(np.vstack(non_normal), columns = ['Non Normal Variable', 'p-value'])
    print(non_normal)
    print(len(non_normal))

    normal = pd.DataFrame(np.vstack(normal), columns = ['Normal Variable', 'p-value'])
    print(normal)
    print(len(normal))

    return(normal, non_normal)

def group_corr_variables(correlations):
    """
    Takes the full correlation table and pairs variables together with their respective correlation values.

    Parameters:
    ----------
        correlation: correlation table

    Returns:
    -------
        dataframe with paired variables and their respective correlations
    
    """
    corr = (
        correlations.where(np.triu(np.ones(correlations.shape), k=1).astype(bool))  # keep upper triangle only
        .stack()                                                 # convert to pairs
        .reset_index()
    )

    corr.columns = ['var_1', 'var_2', 'correlation']

    return(corr)

def set_corr_thresholds(corr_data, range : bool, threshold : int | list):

    """
    Applies absolute thresholds to the full correlation table (see previous function)

    Parameters:
    -----------
        corr_data (DataFrame): datatable with the paired variables and respective correlations
        range (bool): If True, upper and lower thresholds should be applied, if False, the lower limit should be applied
        threshold (int | list): if range == True, a list should be given, with the lower threshold limit first. 
                                If range == False, a single threhsold should be used.

    Returns:
    ---------
        Filtered correlation variables datatable based on given thresholds.   
    
    """

    if range == True:
        result = corr_data[((corr_data['correlation'].abs() > threshold[0])) & (corr_data['correlation'].abs() <= threshold[1])]

    if range == False:
        result = corr_data[corr_data['correlation'].abs() > threshold]

    return(result)


def axis_values_for_variables(data_table, variable_column : str, axis_column : str):

    """
    Converts the variable name to a value for either x or y axes for plotting

    Parameters:
    -----------
        data_table (DataFrame): datatable with paired variables and correlations
        variable_column (str): column name with the variables to apply numerical values for plot axes
        axis_column (str): name of the numeric column for either x or y axes
    
    Returns:
    --------
        Input dataframe with additional column with axes values. 
    """

    result = []

    for num, i in enumerate(np.array(data_table[variable_column].unique())):
        result.append([num, i])

    result = pd.DataFrame(np.vstack(result), columns = [axis_column, variable_column])
    result[axis_column] = result[axis_column].astype(int)

    return(result)

def set_correlation_colours(data_table, corr_column : str, limits : float):
    """
    create correlation colours for plots

    Parameters:
    -----------
        data_table (DataFrame): datatable with paired variables and correlations
        corr_column (str): column that contains the correlation values
        limits (float): upper threshold values for the correlation cutoff
    
    Returns:
    --------
        data_table (DataFrame): correlation and variable datatable with new colour column
        cmap: colourmap for the plots
        norm: center of the colourmap
    
    """
    colour = data_table[corr_column]

    # center the colormap at 0
    norm = mcolors.TwoSlopeNorm(vmin=-limits, vcenter=0, vmax=limits)

    # choose a diverging colormap
    cmap = plt.cm.coolwarm

    # map correlations to RGBA colors
    data_table["colour"] = colour.apply(lambda x: cmap(norm(x)))

    return(data_table, cmap, norm)

def correlation_compare_colourbad(fig, ax, cmap, norm):

    """
    Creates a colourbar based on the figure data.
    
    Parameters:
    -----------
        fig: plot figure
        ax: subplot panel
        cmap: colourmap for the plots
        norm: center of the colourmap

    Returns:
    -------
        Creates a colour bar for the plots
    
    """
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.01)
    # cbar.set_label("Correlation", fontsize=12)
    cbar.ax.tick_params(labelsize=10)

def correlation_compare_plot(data_table, xaxis_column : str, yaxis_column : str, correlation_column : str,
                             var1_labels, var2_column : str, title : str, cmap, norm ):
    
    """
    Creates a plot comparing the variables and their respective correlation values for easy comparison.

    Parameters:
    ----------
        data_table (DataFrmae): table with contestent values
        xaxis_column (str): name of column for x axis
        yaxis_column (str): name of column for y axis
        correlation_column (str): name of column with values correlations
        var1_labels: variable of editted column with first variables for the x axis
        var2_column (str): name of column with second variable (for y axis)
        title (str): title of the plot
        cmap: colourmap for the plots
        norm: center of the colourmap    
    """

    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.13, top = 0.94, left = 0.17, right = 1.05)
    for i in range(len(data_table)):
        text = plt.text(data_table.iloc[i][xaxis_column], data_table.iloc[i][yaxis_column], 
                f"{data_table.iloc[i][correlation_column]:.2f}", fontsize = 13,
                ha="center", va="center", color="white",
                bbox=dict(boxstyle="round,pad=0.3",
                    fc=data_table.iloc[i]["colour"],
                    ec="black",
                    lw=0.7,
                    alpha=0.9))
    plt.xlim(-0.5, data_table[xaxis_column].max() + 0.5)
    plt.ylim(-0.5, data_table[yaxis_column].max() + 0.5)
    plt.xticks(data_table[xaxis_column], var1_labels, fontsize = 10)
    plt.yticks(data_table[yaxis_column], data_table[var2_column], fontsize = 12)
    plt.title(title, fontsize = 20)
    plt.grid(True, linestyle="--", alpha=0.3)
    #colour bar
    correlation_compare_colourbad(fig = fig, ax = ax, cmap = cmap, norm = norm)
    plt.show()

def corr_subplots(data_table, corr_table):

    """
    Creates a figure with scatter subplots for each variable pair

    Parameters:
    -----------
        data_table (DataFrame): table with contestent values
        corr_table (DataFrame): correlation datatable
    
    """

    fig, axes = plt.subplots(nrows = (math.ceil(len(corr_table)/3)), ncols = 3)
    plt.subplots_adjust(wspace=0.3, hspace=0.35, bottom = 0.08, top = 0.98, left = 0.05, right = 0.95)

    for row, ax in enumerate(axes.flatten()[:len(corr_table)]):

        ax.scatter(data_table[corr_table['var_1'][row]], data_table[corr_table['var_2'][row]], 
                color = corr_table['colour'][row]) 
        ax.plot([], [], color = 'white', label = f"{round(corr_table['correlation'][row],2)}")
        ax.set_xlabel(corr_table['var_1'][row])
        ax.set_ylabel(corr_table['var_2'][row])
        legend = ax.legend(frameon=True, loc = 'best', labelcolor = 'white', 
                        facecolor = corr_table['colour'][row])
    if len(corr_table) == 11:   
        fig.delaxes(axes[3][2])
    if len(corr_table) == 5:
        fig.delaxes(axes[1][2])
    plt.show()


def slope(y1, y2, x1, x2):

    """"
    Determines the slope of a straight line

    Parameters:
    -----------
        x1, x2 (int): min and max x values
        y1, y2 (int): min and max y values

    Returns:
    --------
        slope of a line
    
    """
    y = y2 - y1
    x = x2 - x1
    m = y/x
    return(m)

def intercept(y1, x1, slope):
    """"
    Determines the intercept of a straight line

    Parameters:
    -----------
        x1 (int): min x value
        y1 (int): min y value
        slope (int): slope of the line (see function above)

    Returns:
    --------
        y-intercept of a line
    
    """
    b = y1 - x1*slope
    return(b)