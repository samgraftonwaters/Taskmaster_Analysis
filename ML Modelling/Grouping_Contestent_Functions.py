from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def determine_sil_values(k_range, X_data):

    """
    Calculates the set of silhouette score for Kmeans based on range of K clusters

    Parameters:
    -----------
        k_range: range of K clusters. Should start on 2.
        X_data: scaled data
    
    Returns
    -------
        list of solhouette scores for Euclidean and Manhatten methods,
        based on number of clusters K.
    """
    eucl_sil_values = []
    man_sil_values = []

    for k in k_range:
        km_clusterer = KMeans(n_clusters=k, init="random", 
                            max_iter=300, random_state=123)
        labels_pred = km_clusterer.fit_predict(X_data)
        eucl_sil_score = silhouette_score(X_data, labels_pred, metric="euclidean")
        man_sil_score = silhouette_score(X_data, labels_pred, metric="manhattan")
        eucl_sil_values.append(eucl_sil_score)
        man_sil_values.append(man_sil_score)
    return(eucl_sil_values, man_sil_values)

def CH_Index_scores(k_range, X_data):
    """
    Calculates the set of Calinski–Harabasz Index scores for Kmeans based on range of K clusters

    Parameters:
    -----------
        k_range: range of K clusters. Should start on 2.
        X_data: scaled data
    
    Returns
    -------
        list of Calinski–Harabasz Index scores based on number of clusters K.
    """
    scores = []

    for k in k_range:
        kmeans =  KMeans(n_clusters=k, init="random", 
                            max_iter=300, random_state=123)
        labels = kmeans.fit_predict(X_data)
        score = calinski_harabasz_score(X_data, labels)
        scores.append(score)
    return(scores)


def determine_sil_values_agg(k_range, X_data, link_type):

    """
    Calculates the set of silhouette score for Kmeans based on range of K clusters

    Parameters:
    -----------
        k_range: range of K clusters. Should start on 2.
        X_data: scaled data
        link_type (str): type of link method
    
    Returns
    -------
        list of solhouette scores for Euclidean and Manhatten methods,
        based on number of clusters K.
    """
    eucl_sil_values = []
    man_sil_values = []

    for k in k_range:
        km_clusterer_eucl = AgglomerativeClustering(n_clusters=k, linkage=link_type, 
                                               metric = 'euclidean').fit(X_data)
        labels_pred_eucl = km_clusterer_eucl.fit_predict(X_data)

        eucl_sil_score = silhouette_score(X_data, labels_pred_eucl, metric="euclidean")
        eucl_sil_values.append(eucl_sil_score)

        if link_type != 'ward':
            km_clusterer_man = AgglomerativeClustering(n_clusters=k, linkage=link_type, 
                                                metric = 'manhattan').fit(X_data)
            labels_pred_man = km_clusterer_man.fit_predict(X_data)
            
            man_sil_score = silhouette_score(X_data, labels_pred_man, metric="manhattan")
            man_sil_values.append(man_sil_score)
        
    return(eucl_sil_values, man_sil_values)