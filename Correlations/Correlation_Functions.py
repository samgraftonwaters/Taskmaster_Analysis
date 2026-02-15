import pandas as pd
import numpy as np
from scipy import stats
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
import seaborn as sns

def normal_variables(data_table):
    columns = data_table.columns

    non_normal = []
    normal = []

    for cols in columns:
        norm = stats.normaltest(data_table[cols])
        if norm.pvalue < 0.01:
            non_normal.append(cols)
            print(f'{cols} p-value = {norm.pvalue}')
        else:
            normal.append(cols)
            print(f'{cols} p-value = {norm.pvalue}')

    print(non_normal)
    print(len(non_normal))

    print(normal)
    print(len(normal))

    return(normal, non_normal)

def group_corr_variables(correlations):
    corr = (
        correlations.where(np.triu(np.ones(correlations.shape), k=1).astype(bool))  # keep upper triangle only
        .stack()                                                 # convert to pairs
        .reset_index()
    )

    corr.columns = ['var_1', 'var_2', 'correlation']

    return(corr)

def set_corr_thresholds(corr_data, range : bool, threshold : int | list):

    if range == True:
        result = corr_data[((corr_data['correlation'].abs() > threshold[0])) & (corr_data['correlation'].abs() <= threshold[1])]

    if range == False:
        result = corr_data[corr_data['correlation'].abs() > threshold]

    return(result)


def axis_values_for_variables(data_table, variable_column : str, axis_column : str):

    result = []

    for num, i in enumerate(np.array(data_table[variable_column].unique())):
        result.append([num, i])

    result = pd.DataFrame(np.vstack(result), columns = [axis_column, variable_column])
    result[axis_column] = result[axis_column].astype(int)

    return(result)

def set_correlation_colours(data_table, corr_column : str, limits : int):
    colour = data_table[corr_column]

    # center the colormap at 0
    norm = mcolors.TwoSlopeNorm(vmin=-limits, vcenter=0, vmax=limits)

    # choose a diverging colormap
    cmap = plt.cm.coolwarm

    # map correlations to RGBA colors
    data_table["colour"] = colour.apply(lambda x: cmap(norm(x)))

    return(data_table, cmap, norm)

def correlation_compare_colourbad(fig, ax, cmap, norm):
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.01)
    # cbar.set_label("Correlation", fontsize=12)
    cbar.ax.tick_params(labelsize=10)

def correlation_compare_plot(data_table, xaxis_column : str, yaxis_column : str, correlation_column : str,
                             var1_labels, var2_column : str, title : str, cmap, norm ):

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
    plt.xticks(data_table[xaxis_column], var1_labels, fontsize = 12)
    plt.yticks(data_table[yaxis_column], data_table[var2_column], fontsize = 12)
    plt.title(title, fontsize = 20)
    plt.grid(True, linestyle="--", alpha=0.3)
    #colour bar
    correlation_compare_colourbad(fig = fig, ax = ax, cmap = cmap, norm = norm)
    plt.show()

def corr_subplots(data_table, corr_table):

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
        
    # fig.delaxes(axes[3][2])
    plt.show()