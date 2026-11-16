import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def get_pca_weights(data, number_pca_comps):

    """
    Obtains each feature weight using the PCA method..
    
    Parameters:
    -----------
        data (DataFrame): scaled features for modelling
        number_pca_comps (int): Number of PCA components to create
    
    Returns:
    --------
        Returns normalised weights associated with each feature based on the PCA method
    
    """
    pca = PCA(n_components=number_pca_comps)
    pca.fit(data)

    weights = pd.Series(pca.components_[0], index=data.columns)

    # normalise weights
    weights = weights / weights.abs().sum()

    return(weights)

def get_entropy_weights(data):

    """
    Obtains each feature weight using the entropy method.
    
    Parameters:
    -----------
        data (DataFrame): scaled features for modelling
    
    Returns:
    --------
        Returns normalised weights associated with each feature based on the entropy method
    
    """

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
    """
    Shift the scores to start at 0.
    
    Parameters:
    -----------
        data (DataFrame): full contestent modelling table
        score_column_name (str): Name of the column with the scores

    Returns:
    --------
        Contestent scores shifted to set the worst performing contestent to 0.

    """

    shift_score = data[score_column_name] - data[score_column_name].min()
    return(shift_score)

def get_scale_score(data, score_column_name:str):

    """
    Rescales the scores to be between 0 and 100.
    
    Parameters:
    -----------
        data (DataFrame): full contestent modelling table
        score_column_name (str): Name of the column with the scores

    Returns:
    --------
        Contestent scores scaled to be set between 0 and 100.

    """
    scale_score = (
        (data[score_column_name] - data[score_column_name].min()) /
        (data[score_column_name].max() - data[score_column_name].min())
    ) * 100
    return(scale_score)