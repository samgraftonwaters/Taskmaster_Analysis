import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def get_pca_weights(data):
    pca = PCA(n_components=1)
    pca.fit(data)

    weights = pd.Series(pca.components_[0], index=data.columns)

    # normalize weights
    weights = weights / weights.abs().sum()

    return(weights)

def get_entropy_weights(data):

    # convert to probabilities
    P = data / data.sum()

    # entropy
    k = 1 / np.log(len(data))
    entropy = -k * (P * np.log(P + 1e-9)).sum()

    # diversification
    d = 1 - entropy

    # weights
    weights = d / d.sum()
    
    return(weights)

def get_shift_score(data, score_column_name:str):
    shift_score = data[score_column_name] - data[score_column_name].min()
    return(shift_score)

def get_scale_score(data, score_column_name:str):
    scale_score = (
        (data[score_column_name] - data[score_column_name].min()) /
        (data[score_column_name].max() - data[score_column_name].min())
    ) * 100
    return(scale_score)