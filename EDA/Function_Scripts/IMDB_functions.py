import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(data, x_label, y_label, title, min_range, max_range):

    fig = plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.9, left = 0.05, right = 0.95)
    sns.heatmap(
        data,
        cmap= "RdYlGn",
        vmin=min_range, vmax=max_range,
        annot=True,
        fmt=".3f",
        linewidths=0.3,
        linecolor="darkgray",
        mask=data.isnull(),
        cbar_kws={"label": "IMDb Rating Ratio"}
    )

    plt.title(title, fontsize=16, weight="bold")
    plt.xlabel(x_label, fontsize = 14)
    plt.ylabel(y_label, fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.tight_layout()
    plt.show()