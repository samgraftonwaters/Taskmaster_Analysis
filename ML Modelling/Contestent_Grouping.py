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
from Correlations import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')
model_data = model_data[model_data['Series'] != 'S21']
data = pd.DataFrame(model_data)

cluster_data = model_data[['Series', 'Name']].copy()
data = data.select_dtypes(include=[float, int])

scaler = RobustScaler()
data_nums = scaler.fit_transform(data)

data_nums = pd.DataFrame(data_nums, columns=data.columns, index=data.index)

k_values = range(3, 7)

cols_to_drop = [[], ['Score', 'Avg_Score_per_Episodes', 'Team_Score_per_Person'],
                ['Score', 'Avg_Score_per_Episodes', 'Team_Score_per_Person', 'Number_Episodes', 'Number_of_Tasks']]

pca_comps = [2, 3, 4]

feature_names = ['PCA1', 'PCA2', 'PCA3', 'PCA4']

kmeans_clustering_results = []
agg_clustering_results = []

for k in k_values:
    for pca in pca_comps:
        for drop_cols in cols_to_drop:

            pca_model = PCA(n_components=pca)
            X_data = data_nums.drop(drop_cols, axis = 1)
            X_pca = pca_model.fit_transform(X_data)

            kmeans = KMeans(n_clusters=k, init="random", 
                                max_iter=300, random_state=123)
            kmeans.fit(X_pca)
            kmeans_pred = kmeans.fit_predict(X_pca)

            kmeans_ss_eucl = silhouette_score(X = X_pca, labels = kmeans_pred, metric='euclidean')
            kmeans_ss_man = silhouette_score(X = X_pca, labels = kmeans_pred, metric='manhattan')

            kmeans_clustering_results.append({
                'Number of Clusters' : k,
                'Number of PCAs' : pca,
                'K Means Silhouette Score (Eucl)': kmeans_ss_eucl,
                'K Means Silhouette Score (Man)': kmeans_ss_man,
                'Columns Dropped' : drop_cols
            })

        ####################
            cluster_method_euclidean = ['single', 'complete', 'average', 'ward']
            cluster_method_manhattan = ['single', 'complete', 'average']
            
            for link in cluster_method_euclidean:
                agg_model = AgglomerativeClustering(n_clusters=k, linkage=link, 
                                            metric = 'euclidean').fit(X_pca)

                agg_pred = agg_model.fit_predict(X_pca)

                agg_labels = agg_model.labels_

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

kmeans_eucl = kmeans_clustering_results[kmeans_clustering_results['K Means Silhouette Score (Eucl)'] == kmeans_clustering_results['K Means Silhouette Score (Eucl)'].max()]
kmeans_man = kmeans_clustering_results[kmeans_clustering_results['K Means Silhouette Score (Man)'] == kmeans_clustering_results['K Means Silhouette Score (Man)'].max()]

if kmeans_clustering_results['K Means Silhouette Score (Eucl)'].max() > kmeans_clustering_results['K Means Silhouette Score (Man)'].max():
    kmeans_best_model = kmeans_eucl
    print(f"The Euclidean Silhouette Score is: {kmeans_eucl['K Means Silhouette Score (Eucl)']}")
    
else:
    kmeans_best_model = kmeans_man
    print(f"The Manhattan Silhouette Score is: {kmeans_man['K Means Silhouette Score (Man)']}")

print(kmeans_best_model)

agg_best_model = agg_clustering_results[agg_clustering_results['Agg Silhouette Score (Eucl)'] == agg_clustering_results['Agg Silhouette Score (Eucl)'].max()].reset_index(drop = True)
print(agg_best_model)

###########
print()
print('Kmeans Method')

X_data_kmeans = data_nums.drop(columns = kmeans_best_model['Columns Dropped'].iloc[0], axis = 1)

pca_model_kmeans = PCA(n_components=kmeans_best_model['Number of PCAs'].iloc[0])
X_pca_kmeans = pca_model_kmeans.fit_transform(X_data_kmeans)

kmeans = KMeans(n_clusters=kmeans_best_model['Number of Clusters'].iloc[0], init="random", max_iter=300, random_state=123).fit(X_pca_kmeans)

kmeans_labels = kmeans.labels_
centers_scaled = kmeans.cluster_centers_
groups_kmeans = np.unique(kmeans_labels)

cluster_data_kmeans = GCF.get_pca_clusters(data = cluster_data, pca_num = kmeans_best_model['Number of PCAs'].iloc[0], X_pca = X_pca_kmeans)

cluster_data_kmeans[f'Group kmeans'] = kmeans_labels
cluster_data_kmeans = pd.concat([cluster_data_kmeans, data.drop(kmeans_best_model['Columns Dropped'].iloc[0], axis = 1)], axis = 1)

kmeans_centers_df = pd.DataFrame(centers_scaled, columns=feature_names[0:kmeans_best_model['Number of PCAs'].iloc[0]])

print(kmeans_centers_df)
print(cluster_data_kmeans.head())

#########
print()
print('Agglomerative Method')

X_data_agg = data_nums.drop(agg_best_model['Columns Dropped'].iloc[0], axis = 1)

pca_model_agg = PCA(n_components=agg_best_model['Number of PCAs'].iloc[0])
X_pca_agg = pca_model_agg.fit_transform(X_data_agg)

agg_model = AgglomerativeClustering(n_clusters=agg_best_model['Number of Clusters'].iloc[0], linkage=agg_best_model['Agg Link'].iloc[0], 
                            metric = 'euclidean').fit(X_pca_agg)

agg_labels = agg_model.labels_
groups_agg = np.unique(agg_labels)

cluster_data_agg = GCF.get_pca_clusters(data = cluster_data, pca_num = agg_best_model['Number of PCAs'].iloc[0], X_pca = X_pca_agg)

cluster_data_agg[f'Group Agg'] = agg_labels
cluster_data_agg = pd.concat([cluster_data_agg, data.drop(agg_best_model['Columns Dropped'].iloc[0], axis = 1)], axis = 1)


agg_centers = cluster_data_agg.groupby('Group Agg')[feature_names[0:agg_best_model['Number of PCAs'].iloc[0]]].mean()

agg_centers_df = pd.DataFrame(agg_centers, columns=feature_names[0:agg_best_model['Number of PCAs'].iloc[0]])


print(agg_centers_df)
print(cluster_data_agg.head())

colours = plt.cm.tab10.colors

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_kmeans, colours):
    plt.scatter(cluster_data_kmeans[cluster_data_kmeans['Group kmeans']==group][feature_names[0]], 
                cluster_data_kmeans[cluster_data_kmeans['Group kmeans']==group][feature_names[1]], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

    plt.scatter(kmeans_centers_df.iloc[[group]][feature_names[0]], kmeans_centers_df.iloc[[group]][feature_names[1]], 
                marker ='*', s = 450, color=colour, edgecolor = 'black',
                label = f'Class {group} Center')

plt.legend(fontsize = 15, ncols = 3)
plt.title(f'Comparing Kmeans clusters', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_agg, colours):
    plt.scatter(cluster_data_agg[cluster_data_agg['Group Agg']==group][feature_names[0]], 
                cluster_data_agg[cluster_data_agg['Group Agg']==group][feature_names[1]], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

    plt.scatter(agg_centers_df.iloc[[group]][feature_names[0]], agg_centers_df.iloc[[group]][feature_names[1]], 
                marker ='*', s = 450, color=colour, edgecolor = 'black',
                label = f'Class {group} Center')

plt.legend(fontsize = 15, ncols = 3)
plt.title(f'Comparing Agg clusters', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

cluster_data_kmeans.to_csv(file_path + 'Contestent_Clustering_kmeans.csv', sep = ',', index = False)
cluster_data_agg.to_csv(file_path + 'Contestent_Clustering_Agg.csv', sep = ',', index = False)

kmeans_best_model.to_csv(file_path + 'kmeans_model_parameters.csv', sep = ',', index = False)
agg_best_model.to_csv(file_path + 'agg_model_parameters.csv', sep = ',', index = False)

# cluster_data_kmeans.to_csv(file_path + 'Contestent_Clustering_kmeans_REMOVE5COLS.csv', sep = ',', index = False)
# cluster_data_agg.to_csv(file_path + 'Contestent_Clustering_Agg_REMOVE5COLS.csv', sep = ',', index = False)

# kmeans_best_model.to_csv(file_path + 'kmeans_model_parameters_REMOVE5COLS.csv', sep = ',', index = False)
# agg_best_model.to_csv(file_path + 'agg_model_parameters_REMOVE5COLS.csv', sep = ',', index = False)