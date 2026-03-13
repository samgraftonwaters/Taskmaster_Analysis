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

#Selecting only Numerical Data
data_nums = data.select_dtypes(include=[float, int])

# # PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(data_nums)

data["PCA1"] = X_pca[:,0]
data["PCA2"] = X_pca[:,1]

k_values = range(2, 12)


sil_values_kmeans = GCF.determine_sil_values(k_range = k_values, X_data = X_pca)

print(sil_values_kmeans)
print()
print(print(sil_values_kmeans[1]))

ch_scores_kmeans = GCF.CH_Index_scores(k_range = k_values, X_data = X_pca)



GCF.plot_silhouette_scores(k = k_values, silhouette_values = sil_values_kmeans, 
                       labels = ['Euclidean', 'Manhattan'], colours = ['darkgreen', 'dodgerblue'],
                       title = "Kmeans Silhouette Scores for different Ks")

#Calinski–Harabasz Index



fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

plt.plot(k_values, ch_scores_kmeans, marker='o', lw = 3, markersize = 10)
plt.title("Calinski–Harabasz Index for different K", fontsize = 22)
plt.xlabel("Number of clusters (K)", fontsize = 16)
plt.ylabel("Calinski–Harabasz Index", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()