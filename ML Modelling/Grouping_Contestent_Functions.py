from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def determine_kmeans_sil_values(k_range, X_data, distance_method):

    """
    Calculates the set of silhouette score for Kmeans based on range of K clusters

    Parameters:
    -----------
        k_range: range of K clusters. Should start on 2.
        X_data: scaled data
        distance_method (str): type of distance method. e.g. Euclidean or Manhattan
    
    Returns
    -------
        list of solhouette scores for kmeans model based on specified distance method, for
        a number of clusters K.
    """
    sil_values = []

    for k in k_range:
        km_clusterer = KMeans(n_clusters=k, init="random", 
                            max_iter=300, random_state=123)
        labels_pred = km_clusterer.fit_predict(X_data)
        sil_score = silhouette_score(X_data, labels_pred, metric=distance_method)
        sil_values.append(sil_score)

    return(sil_values)

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

def plot_clustering_line_graphs(x_values, y_values, labels, colours, title, y_label, x_label, ncol = 1):

    """
    Plots line graphs of silhouette score for each cluster value

    Parameters:
    -----------
        x_values: data for x-axis
        y_values: data for y-axis
        labels: list of labels for each line
        colours: list of colours for each line
        title (str): plot title
        y_label (str): labels of y axis
        x_label (str): label of x axis
        ncol (int): number of columns for the legend. Default = 1

    Results:
    --------
        Plots set of line graphs for clustering models. e.g. Silhouette score against number of 
        clusters k.
    """
    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.98)

    try:
        for y, colour, label in zip(y_values, colours, labels):
            plt.plot(x_values, y, color = colour, label = label, 
                    marker = 'o', lw = 3, markersize = 12)
    except:
        plt.plot(x_values, y_values, color = colour, label = labels, 
                    marker = 'o', lw = 3, markersize = 12)

    plt.title(title, fontsize = 22)
    plt.xlabel(x_label, fontsize = 16)
    plt.ylabel(y_label, fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend(fontsize = 15, ncol = ncol)
    plt.show()

def get_dbscan_silhouette_epsilon_values(X_data, epsilon_range, distance_method):

    """
    Gets the silhouette scores and reach distances (epsilon) for the DBSCAN classification model

    Parameters:
    -----------
        X_data: X variables for the classification model
        epsilon_range: range of reach distances to iterate over
        distance_method (str): type of distance method. e.g. Euclidean or Manhattan
    
    Returns:
    --------
        sil_values: Silhouette score values (for each reach distance value)
        eps_values: reach distances for dbscan classification model.
    
    """

    sil_values = []
    eps_values = []

    for reach_dist in epsilon_range:
    
        dbscan_model = DBSCAN(eps=reach_dist, metric=distance_method).fit(X_data)
        labels_pred = dbscan_model.labels_

        if len(np.unique(labels_pred)) > 1:
            sil_score = silhouette_score(X_data, labels_pred, metric=distance_method)
            eps_values.append(reach_dist)
            sil_values.append(sil_score)
        
    return(sil_values, eps_values)


def determine_sil_values_agg_both_distance_methods(k_range, X_data, link_type):

    """
    Calculates the set of silhouette score for Hierarchical Clustering based on range of K clusters

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


def determine_sil_values_agg(k_range, X_data, link_type, distance_method):

    """
    Calculates the set of silhouette score for Hierarchical Clustering based on range of K clusters

    Parameters:
    -----------
        k_range: range of K clusters. Should start on 2.
        X_data: scaled data
        link_type (str): type of link method
        distance_method (str): type of distance method. e.g. Euclidean or Manhattan
    
    Returns
    -------
        list of solhouette scores for Euclidean and Manhatten methods,
        based on number of clusters K.
    """
    sil_values = []

    for k in k_range:
        km_clusterer = AgglomerativeClustering(n_clusters=k, linkage=link_type, 
                                               metric = distance_method).fit(X_data)
        labels_pred = km_clusterer.fit_predict(X_data)

        sil_score = silhouette_score(X_data, labels_pred, metric=distance_method)
        sil_values.append(sil_score)
        
    return(sil_values)


def plot_bar_groups(dataframe, average_metric : str):

    """
    Plot each metric to determine group cluster's actual meaning

    Parameters:
    ----------
        dataframe (DataFrame): contains dataframe with group, metrics, average and median columns
        average_metric (str): name of the column to plot data from ('Average' or 'Median') 
    
    Returns:
    --------
        bar chart comparing the values of each metric between the groups
    
    """
    pivot = dataframe.pivot(index="Group", columns="Metric", values=average_metric)

    groups = pivot.index.values

    # Extract each metric
    score = pivot["Score"]
    position = pivot["Position"]
    rescale = pivot["final_score_rescale"]
    rank = pivot["Contestent Rank"]

    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.92, left = 0.07, right = 0.98)

    bar1 = plt.bar(groups - 0.30, score, width=0.18, edgecolor='black', label='Score')
    bar2 = plt.bar(groups - 0.10, position, width=0.18, edgecolor='black', label='Position')
    bar3 = plt.bar(groups + 0.10, rescale, width=0.18, edgecolor='black', label='Final Score Rescale')
    bar4 = plt.bar(groups + 0.30, rank, width=0.18, edgecolor='black', label='Contestant Rank')

    for bars in [bar1, bar2, bar3, bar4]:
        plt.bar_label(bars, fmt='%.2f', fontsize=12, color = 'black', label_type='edge')

    plt.xticks(groups, fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel('Group', fontsize=18)
    plt.ylabel(f'{average_metric} Value', fontsize=18)
    plt.title(f'{average_metric} Metrics by Group', fontsize=22)

    plt.legend(fontsize = 15, ncol = 2)
    plt.show()