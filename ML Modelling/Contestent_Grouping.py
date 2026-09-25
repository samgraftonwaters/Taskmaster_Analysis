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

data_nums = data.select_dtypes(include=[float, int])
print(data_nums.columns)

k_values = range(2, 12)

X_data = data_nums

axes_pars = ['Avg_Score_per_Episodes', 'Team_Score_per_Person']

par1_idx = X_data.columns.get_loc(axes_pars[0])
par2_idx = X_data.columns.get_loc(axes_pars[0])

print()
#####
#1. Kmeans Method
#####

print('Kmeans Method')
sil_values_kmeans_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_data, 
                                                         distance_method = 'euclidean')

sil_values_kmeans_man = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X_data, 
                                                         distance_method = 'manhattan')

GCF.plot_clustering_line_graphs(x_values = k_values, y_values = [sil_values_kmeans_eucl, sil_values_kmeans_man], 
                       labels = ['Euclidean', 'Manhattan'], colours = ['darkgreen', 'dodgerblue'],
                       title = "Kmeans Silhouette Scores for different Number of Clusters (K)",
                       x_label = "Number of Clusters (K)", y_label = "Silhoette Score")



kmeans = KMeans(n_clusters=3)#sil_max_K_value_kmeans)
kmeans.fit(X_data)

kmeans_labels = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

X_data['Group'] = kmeans_labels

groups_kmeans = np.unique(kmeans_labels)
print(groups_kmeans)


feature_names = [par1_idx, par2_idx]
centers_df = pd.DataFrame(centers_scaled[:, feature_names], columns=axes_pars)

print(centers_df)

colours = plt.cm.tab10.colors

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_kmeans, colours):
    plt.scatter(X_data[X_data['Group']==group][axes_pars[0]], 
                X_data[X_data['Group']==group][axes_pars[1]], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

    plt.scatter(centers_df.iloc[[group]][axes_pars[0]], centers_df.iloc[[group]][axes_pars[1]], 
                marker ='*', s = 450, color=colour, edgecolor = 'black',
                label = f'Class {group} Center')

plt.legend(fontsize = 15, ncols = 2)
plt.title(f'Comparing Kmeans clusters', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()