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

print(model_data.head())

print(model_data.info())

print(model_data.columns)

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
    print("Best Sillhouette Score (Euclidean):", round(max(sil_values_kmeans_eucl), 4))
    print("Best Sillhouette K (Euclidean):", sil_max_K_value)

else:
    kmeans_distance_method = 'manhattan'
    sil_max_K_value = max(zip(k_values, sil_values_kmeans_man), key=lambda x: x[1])[0]
    print("Best Sillhouette Score (Manhattan):", round(max(sil_values_kmeans_man), 4))
    print("Best Sillhouette K (Manhattan):", sil_max_K_value)


# ---- Run KMeans ----
kmeans = KMeans(n_clusters=sil_max_K_value)
kmeans.fit(X_pca)

cluster_data ['Group (kmeans)'] = kmeans.labels_
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
    plt.scatter(cluster_data[cluster_data['Group (kmeans)']==group]['PCA1'], 
                cluster_data[cluster_data['Group (kmeans)']==group]['PCA2'], label = f'Class {group}',
                color = colour)

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

# Produce baseline true value silhouette scores
sil_score = silhouette_score(X_pca, kmeans_labels, metric="kmeans_distance_method")

print(f"{kmeans_distance_method} Silhouette Score: ", round(sil_score, 4))
print()



#####
#2. DBSCAN Method
#####
print('DBSCAN Method')

possible_eps_values = np.linspace(start=0.1, stop=15, num=100)

dbscan_eucl_sil_values, eps_values_eucl = GCF.get_dbscan_silhouette_epsilon_values(X = X_pca, epsilon_range = possible_eps_values, distance_method = 'euclidean')
dbscan_man_sil_values, eps_values_man = GCF.get_dbscan_silhouette_epsilon_values(X = X_pca, epsilon_range = possible_eps_values, distance_method = 'manhattan')


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

eucl_eps_max = max(zip(eps_values_eucl, dbscan_eucl_sil_values), key=lambda x: x[1])[0]
man_eps_max = max(zip(eps_values_man, dbscan_man_sil_values), key=lambda x: x[1])[0]

print(r"Best Euclidean Reach Distance ($\epsilon$)", eucl_eps_max)
print(r"Best Manhattan Reach Distance ($\epsilon$)", man_eps_max)

#-----Run DBSCAN-----

dbscan_eucl = DBSCAN(eps=eucl_eps_max, metric="euclidean", min_samples=20)
dbscan_eucl.fit(X_pca)

cluster_data['Group (dbscan eucl)'] = dbscan_eucl.labels_
dbscan_labels_eucl = dbscan_eucl.labels_
groups_eucl = np.unique(dbscan_labels_eucl)
print(groups_eucl)

dbscan_man = DBSCAN(eps=man_eps_max, metric="manhattan", min_samples=20)
dbscan_man.fit(X_pca)

cluster_data['Group (dbscan man)'] = dbscan_man.labels_
dbscan_labels_man = dbscan_man.labels_
groups_man = np.unique(dbscan_labels_man)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_eucl, colours):
    
    plt.scatter(cluster_data[cluster_data['Group (dbscan eucl)']==group]['PCA1'], 
                cluster_data[cluster_data['Group (dbscan eucl)']==group]['PCA2'], 
                label = f'Class {group}', color = colour)

plt.legend(fontsize = 15)
plt.title('Comparing DBSCAN clusters with "Euclidean" Method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_man, colours):
    plt.scatter(cluster_data[cluster_data['Group (dbscan man)']==group]['PCA1'], 
                cluster_data[cluster_data['Group (dbscan man)']==group]['PCA2'], 
                label = f'Class {group}', color = colour)

plt.legend(fontsize = 15)
plt.title('Comparing DBSCAN clusters with "Manhattan" Method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()
