from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import Grouping_Contestent_Functions as GCF

import sys
sys.path.append('/Users/SamWaters/Documents/Data Science/Taskmaster/')
# sys.path.append("../..")
from Correlations import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')

data = pd.DataFrame(model_data)

cluster_data = model_data[['Series', 'Name']].copy()

#Selecting only Numerical Data
data_nums = data.select_dtypes(include=[float, int])

# # PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(data_nums)

cluster_data["PCA1"] = X_pca[:,0]
cluster_data["PCA2"] = X_pca[:,1]

k_values = range(2, 12)

#####
#1. Kmeans Method
#####

print('Kmeans Method')
sil_values_kmeans_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_pca, 
                                                         distance_method = 'euclidean')

sil_values_kmeans_man = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_pca, 
                                                         distance_method = 'manhattan')

GCF.plot_clustering_line_graphs(x_values = k_values, y_values = [sil_values_kmeans_eucl, sil_values_kmeans_man], 
                       labels = ['Euclidean', 'Manhattan'], colours = ['darkgreen', 'dodgerblue'],
                       title = "Kmeans Silhouette Scores for different Number of Clusters (K)",
                       x_label = "Number of Clusters (K)", y_label = "Silhoette Score")


if max(sil_values_kmeans_eucl) > max(sil_values_kmeans_man):
    kmeans_distance_method = 'euclidean'
    sil_max_K_value = max(zip(k_values, sil_values_kmeans_eucl), key=lambda x: x[1])[0]
    print("Best Euclidean Sillhouette Score:", round(max(sil_values_kmeans_eucl), 4))
    print("Best Euclidean Sillhouette K:", sil_max_K_value)

else:
    kmeans_distance_method = 'manhattan'
    sil_max_K_value = max(zip(k_values, sil_values_kmeans_man), key=lambda x: x[1])[0]
    print("Best Manhattan Sillhouette Score:", round(max(sil_values_kmeans_man), 4))
    print("Best Manhattan Sillhouette K:", sil_max_K_value)


# ---- Run KMeans ----
kmeans = KMeans(n_clusters=sil_max_K_value)
kmeans.fit(X_pca)

cluster_data[f'Group (kmeans {kmeans_distance_method})'] = kmeans.labels_
kmeans_labels = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

groups = np.unique(kmeans.labels_)
print(groups)

feature_names = ['PCA1', 'PCA2']
centers_df = pd.DataFrame(centers_scaled, columns=feature_names)

colours = ['dodgerblue', 'darkorange', 'green', 'blueviolet', 'red', 'magenta']

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups, colours):
    plt.scatter(cluster_data[cluster_data[f'Group (kmeans {kmeans_distance_method})']==group]['PCA1'], 
                cluster_data[cluster_data[f'Group (kmeans {kmeans_distance_method})']==group]['PCA2'], 
                label = f'Class {group}', color = colour)

    plt.scatter(centers_df.iloc[[group]]['PCA1'], centers_df.iloc[[group]]['PCA2'], 
                marker ='*', s = 300, color=colour, edgecolor = 'black',
                label = f'Class {group} Center')

plt.legend(fontsize = 15, ncols = 2)
plt.title(f'Comparing Kmeans clusters using the {kmeans_distance_method} distance method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


#####
#2. DBSCAN Method
#####
print('DBSCAN Method')

possible_eps_values = np.linspace(start=0.1, stop=15, num=100)

dbscan_eucl_sil_values, eps_values_eucl = GCF.get_dbscan_silhouette_epsilon_values(X_data = X_pca, epsilon_range = possible_eps_values, distance_method = 'euclidean')
dbscan_man_sil_values, eps_values_man = GCF.get_dbscan_silhouette_epsilon_values(X_data = X_pca, epsilon_range = possible_eps_values, distance_method = 'manhattan')

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.98)
plt.plot(eps_values_eucl, dbscan_eucl_sil_values, c="blueviolet", label = 'Euclidean', lw = 3)
plt.plot(eps_values_man, dbscan_man_sil_values, c="dodgerblue", label = 'Manhattan', lw = 3)
plt.title("Silhouette Score for different Reach Distances", fontsize = 22)
plt.xlabel(r"Reach Distance ($\epsilon$)", fontsize = 16)
plt.ylabel("Silhoette Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 16)
plt.show()


if max(dbscan_eucl_sil_values) > max(dbscan_man_sil_values):
    dbscan_distance_method = 'euclidean'
    eps_max = max(zip(eps_values_eucl, dbscan_eucl_sil_values), key=lambda x: x[1])[0]
    print("Best Euclidean Silhouette Score: ", round(max(dbscan_eucl_sil_values), 4))
    print(r"Best Euclidean Reach Distance ($\epsilon$)", eps_max)

else:
    dbscan_distance_method = 'Manhattan'
    eps_max = max(zip(eps_values_man, dbscan_man_sil_values), key=lambda x: x[1])[0]
    print("Best Manhattan Silhouette Score: ", round(max(dbscan_man_sil_values), 4))
    print(r"Best Manhattan Reach Distance ($\epsilon$)", eps_max)

#-----Run DBSCAN-----

dbscan = DBSCAN(eps=eps_max, metric=dbscan_distance_method)
dbscan.fit(X_pca)

cluster_data[f'Group (dbscan {dbscan_distance_method})'] = dbscan.labels_
dbscan_labels = dbscan.labels_
groups = np.unique(dbscan_labels)
print(groups)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups, colours):
    
    plt.scatter(cluster_data[cluster_data[f'Group (dbscan {dbscan_distance_method})']==group]['PCA1'], 
                cluster_data[cluster_data[f'Group (dbscan {dbscan_distance_method})']==group]['PCA2'], 
                label = f'Class {group}', color = colour)

plt.legend(fontsize = 15)
plt.title(f'Comparing DBSCAN clusters with {dbscan_distance_method} distance method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()



#######
#3.Hierarchical Clustering
########
print('Hierarchical Clustering Method')

#Create model for each linkage method

single = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = 'single')
complete = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = 'complete')
average = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = 'average')
ward = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = 'ward')

cluster_method = ['single', 'complete', 'average', 'ward']

eucl_agg_sil_values = []
max_k_agg = []
for cluster in cluster_method:
    eucl_agg = GCF.determine_sil_values_agg_2(k_range = k_values, X_data = X_pca, link_type = cluster, 
                                 distance_method = 'euclidean')
    eucl_agg_sil_values.append(eucl_agg)
    k_agg_max = max(zip(k_values, eucl_agg), key=lambda x: x[1])[0]
    max_k_agg.append(k_agg_max)



print(eucl_agg_sil_values)
print(max_k_agg)
