from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Function_Scripts import Grouping_Contestent_Functions as GCF

import sys
sys.path.append('/Users/SamWaters/Documents/Data Science/Taskmaster/')
# sys.path.append("../..")
from Correlations import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
model_data = model_data[model_data['Series'] != 'S21']
data = pd.DataFrame(model_data)

cluster_data = model_data[['Series', 'Name']].copy()
data_nums = data.select_dtypes(include=[float, int])

k_values = range(2, 7)

cols_to_drop = [[], ['Score', 'Avg_Score_per_Episodes', 'Team_Score_per_Person'],
                ['Score', 'Avg_Score_per_Episodes', 'Team_Score_per_Person', 'Number_Episodes', 'Number_of_Tasks']]

pca_comps = [2, 3, 4]

kmeans_clustering_results = []
agg_clustering_results = []

for k in k_values:
    for pca in pca_comps:
        for drop_cols in cols_to_drop:

            pca_model = PCA(n_components=pca)
            X_data = data_nums.drop(drop_cols, axis = 1)
            print(X_data.columns)
            X_pca = pca_model.fit_transform(X_data)

            if pca == 2:

                cluster_data["PCA1"] = X_pca[:,0]
                cluster_data["PCA2"] = X_pca[:,1]

            if pca == 3:
                cluster_data["PCA1"] = X_pca[:,0]
                cluster_data["PCA2"] = X_pca[:,1]
                cluster_data["PCA3"] = X_pca[:,2]

            if pca == 4:
                cluster_data["PCA1"] = X_pca[:,0]
                cluster_data["PCA2"] = X_pca[:,1]
                cluster_data["PCA3"] = X_pca[:,2]
                cluster_data["PCA4"] = X_pca[:,3]

            feature_names = ['PCA1', 'PCA2', 'PCA3', 'PCA4']

            print()
            print('Kmeans Method')

            kmeans = KMeans(n_clusters=k, init="random", 
                                max_iter=300, random_state=123)
            kmeans.fit(X_pca)
            kmeans_pred = kmeans.fit_predict(X_pca)

            kmeans_labels = kmeans.labels_
            centers_scaled = kmeans.cluster_centers_

            # X_data['kmeans Group'] = kmeans_labels
            cluster_data[f'Group kmeans'] = kmeans_labels

            groups_kmeans = np.unique(kmeans_labels)
            print(groups_kmeans)

            print(feature_names[0:pca])

            kmeans_centers_df = pd.DataFrame(centers_scaled, columns=feature_names[0:pca])

            print(kmeans_centers_df)

            kmeans_ss_eucl = silhouette_score(X = X_pca, labels = kmeans_pred, metric='euclidean')
            kmeans_ss_man = silhouette_score(X = X_pca, labels = kmeans_pred, metric='manhattan')

            kmeans_clustering_results.append({
                'Number of Clusters' : k,
                'Number of PCAs' : pca,
                'K Means Silhouette Score (Eucl)': kmeans_ss_eucl,
                'K Means Silhouette Score (Man)': kmeans_ss_man,
                'Columns Dropped' : drop_cols
            })

            print()
            print('Agglomerative Method')
            cluster_method_euclidean = ['single', 'complete', 'average', 'ward']
            cluster_method_manhattan = ['single', 'complete', 'average']
            
            for link in cluster_method_euclidean:
                agg_model = AgglomerativeClustering(n_clusters=k, linkage=link, 
                                            metric = 'euclidean').fit(X_pca)

                agg_pred = agg_model.fit_predict(X_pca)

                #Access labels assigned for each method
                agg_labels = agg_model.labels_
                cluster_data[f'Group Agg'] = agg_labels
                groups_agg = np.unique(agg_labels)
                # print(groups_agg)

                agg_centers = cluster_data.groupby('Group Agg')[feature_names[0:pca]].mean()

                agg_centers_df = pd.DataFrame(agg_centers, columns=feature_names[0:pca])

                print(agg_centers_df)

                agg_ss_eucl = silhouette_score(X = X_pca, labels = agg_pred, metric='euclidean')
                # agg_ss_man = silhouette_score(X = X_pca, labels = agg_pred, metric='manhattan')

                agg_clustering_results.append({
                    'Number of Clusters' : k,
                    'Number of PCAs' : pca,
        
                    'Agg Silhouette Score (Eucl)' : agg_ss_eucl,
                    # 'Agg Silhouette Score (man)' : agg_ss_man,
                    'Agg Link' : link,
                    'Columns Dropped' : drop_cols

                })

kmeans_clustering_results = pd.DataFrame(kmeans_clustering_results)
agg_clustering_results = pd.DataFrame(agg_clustering_results)
print(kmeans_clustering_results)
print(agg_clustering_results)



# for k, pca in zip(k_values, pca_comps):

#     pca_model = PCA(n_components=pca)
#     X_pca = pca_model.fit_transform(X_data)

#     if pca == 2:

#         cluster_data["PCA1"] = X_pca[:,0]
#         cluster_data["PCA2"] = X_pca[:,1]

#     if pca == 3:
#         cluster_data["PCA1"] = X_pca[:,0]
#         cluster_data["PCA2"] = X_pca[:,1]
#         cluster_data["PCA3"] = X_pca[:,2]

#     if pca == 4:
#         cluster_data["PCA1"] = X_pca[:,0]
#         cluster_data["PCA2"] = X_pca[:,1]
#         cluster_data["PCA3"] = X_pca[:,2]
#         cluster_data["PCA4"] = X_pca[:,3]

#     feature_names = ['PCA1', 'PCA2', 'PCA3', 'PCA4']

#     print()
#     #####
#     #1. Kmeans Method
#     #####

#     print('Kmeans Method')
#     sil_values_kmeans_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_pca, 
#                                                             distance_method = 'euclidean')

#     sil_values_kmeans_man = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_pca, 
#                                                             distance_method = 'manhattan')

#     GCF.plot_clustering_line_graphs(x_values = k_values, y_values = [sil_values_kmeans_eucl, sil_values_kmeans_man], 
#                         labels = ['Euclidean', 'Manhattan'], colours = ['darkgreen', 'dodgerblue'],
#                         title = "Kmeans Silhouette Scores for different Number of Clusters (K)",
#                         x_label = "Number of Clusters (K)", y_label = "Silhoette Score")



#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(X_pca)

#     kmeans_labels = kmeans.labels_
#     centers_scaled = kmeans.cluster_centers_

#     # X_data['kmeans Group'] = kmeans_labels
#     cluster_data[f'Group kmeans'] = kmeans_labels

#     groups_kmeans = np.unique(kmeans_labels)
#     print(groups_kmeans)

#     print(feature_names[0:pca])

#     kmeans_centers_df = pd.DataFrame(centers_scaled, columns=feature_names[0:pca])

#     print(kmeans_centers_df)

#     print()
#     print('Agglomerative Method')
#     cluster_method_euclidean = ['single', 'complete', 'average', 'ward']
#     cluster_method_manhattan = ['single', 'complete', 'average']

#     for link in cluster_method_manhattan:
#         agg_model = AgglomerativeClustering(n_clusters=k, linkage=link, 
#                                     metric = 'manhattan').fit(X_data)

#         #Access labels assigned for each method
#         agg_labels = agg_model.labels_
#         cluster_data[f'Group Agg'] = agg_labels
#         groups_agg = np.unique(agg_labels)
#         print(groups_agg)

#         centers = cluster_data.groupby('Group Agg')[feature_names[0:pca]].mean()

#         agg_centers_df = pd.DataFrame(centers_scaled, columns=feature_names[0:pca])

#         print(kmeans_centers_df)

# centers = cluster_data.groupby(f'Group (Agg {agg_distance_method} {agg_cluster_method})')[["PCA1","PCA2"]].mean()
































# colours = plt.cm.tab10.colors

# fig, ax = plt.subplots()
# plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

# for group, colour in zip(groups_kmeans, colours):
#     plt.scatter(X_data[X_data['Group']==group][axes_pars[0]], 
#                 X_data[X_data['Group']==group][axes_pars[1]], 
#                 label = f'Class {group}', color = colour, marker = 'o', s = 50)

#     plt.scatter(centers_df.iloc[[group]][axes_pars[0]], centers_df.iloc[[group]][axes_pars[1]], 
#                 marker ='*', s = 450, color=colour, edgecolor = 'black',
#                 label = f'Class {group} Center')

# plt.legend(fontsize = 15, ncols = 2)
# plt.title(f'Comparing Kmeans clusters', fontsize = 22)
# plt.xlabel("PCA1", fontsize = 16)
# plt.ylabel("PCA2", fontsize = 16)
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.show()