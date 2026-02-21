from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('/Users/SamWaters/Documents/Data Science/Taskmaster/')
# sys.path.append("../..")
from Correlations import Correlation_Functions as CF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(model_data.head())

print(model_data.info())

print(model_data.columns)

data = model_data.drop(['Series', 'Name'], axis = 1)

data = pd.DataFrame(data)

#Selecting only Numerical Data
data_nums = data.select_dtypes(include=[float, int])

#Determining Correlations
correlations = data_nums.corr(method = 'spearman')
grouped_variables = CF.group_corr_variables(correlations = correlations)
print('Correlation > 0.7:')
print(CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.7))
print('\nCorrelation > 0.9:')
print(CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.9))

#Splitting variables into scalable or not
scaled_cols = ['Score', 'Avg Score per Episodes',
       'Avg Score per Tasks', 'Number 5s Scored', 'Number 1s Scored',
       'Tie Break Wins', 'Tie Break Losses', 
       'Tie Breaks per series', 'Disqualifications', 'Number_Episodes',
       'Episode Percentage Wins', 'Episode Percentage Lossses',
       'Number Team Tasks', 'Team Total', 'Team Score per Person Task']

cat_cols= ['Position']

ohe_cols = ['Team_A', 'Age_Ranges_20 - 29', 'Age_Ranges_30 - 39',
       'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 'Age_Ranges_60 - 69',
       'Gender_Female', 'Gender_Non-Binary', 'Seat_Seat 1',
       'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5']

#Removed Team_B, Tie Breaks per Person and Gender_male as these are highly correlated

preprocessor = ColumnTransformer(
    transformers=[
        ('num', RobustScaler(), scaled_cols),              # numeric → scale
        ('cat', 'passthrough', cat_cols),  # raw categorical → OHE
        ('ohe', 'passthrough', ohe_cols)                  # already OHE → keep
    ]
)

#Transform the data
X_scaled = preprocessor.fit_transform(data)

k_values = range(2, 12)

#Silhouette Scores
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

sil_values_kmeans = determine_sil_values(k_range = k_values, X_data = X_scaled)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

plt.plot(k_values, sil_values_kmeans[0], c="darkgreen", marker='o', label = 'Euclidean',
          lw = 3, markersize = 10)
plt.plot(k_values, sil_values_kmeans[1], c="dodgerblue", marker='o', label = 'Manhattan', 
         lw = 3, markersize = 10)

plt.title("Silhouette Score for different K", fontsize = 22)
plt.xlabel("Number of Clusters (K)", fontsize = 16)
plt.ylabel("Silhoette Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 16)
plt.show()

#Calinski–Harabasz Index

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

ch_scores_kmeans = CH_Index_scores(k_range = k_values, X_data = X_scaled)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

plt.plot(k_values, ch_scores_kmeans, marker='o', lw = 3, markersize = 10)
plt.title("Calinski–Harabasz Index for different K", fontsize = 22)
plt.xlabel("Number of clusters (K)", fontsize = 16)
plt.ylabel("Calinski–Harabasz Index", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

sil_max_K_value = max(zip(k_values, sil_values_kmeans), key=lambda x: x[1])[0]
ch_max_K_value = max(zip(k_values, ch_scores_kmeans), key=lambda x: x[1])[0]

print("Best Sillhouette K:", sil_max_K_value)
print("Best Calinski–Harabasz K:", ch_max_K_value)

# ---- Run KMeans ----
kmeans = KMeans(n_clusters=sil_max_K_value, random_state=42, n_init='auto')
kmeans.fit(X_scaled)

data['Group (kmeans)'] = kmeans.labels_
kmeans_labels = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

feature_names = scaled_cols + ohe_cols + cat_cols
centers_df = pd.DataFrame(centers_scaled, columns=feature_names)

scaler = preprocessor.named_transformers_['num']
centers_df[scaled_cols] = scaler.inverse_transform(centers_df[scaled_cols])

print(centers_df)
print(centers_df.iloc[[0]])
print(centers_df.iloc[[2]])

class0 = data[data['Group (kmeans)']==0]
class1 = data[data['Group (kmeans)']==1]
class2 = data[data['Group (kmeans)']==2]

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)
plt.scatter(class0['Number 5s Scored'], class0['Score'], label = 'class 0')
plt.scatter(class1['Number 5s Scored'], class1['Score'], label = 'class 1')
plt.scatter(class2['Number 5s Scored'], class2['Score'], label = 'class 2')

plt.scatter(centers_df.iloc[[0]]['Number 5s Scored'], centers_df.iloc[[0]]['Score'], marker ='*', 
            s = 300, color='blue')
plt.scatter(centers_df.iloc[[1]]['Number 5s Scored'], centers_df.iloc[[1]]['Score'], marker ='*', 
            s = 300, color='darkorange')
plt.scatter(centers_df.iloc[[2]]['Number 5s Scored'], centers_df.iloc[[2]]['Score'], marker ='*', 
            s = 300, color='green')

plt.legend(fontsize = 15)
plt.title('Comparing Kmeans clusters for Total Score against Number of 5s Scored', fontsize = 22)
plt.xlabel("Number of 5s Scored", fontsize = 16)
plt.ylabel("Total Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


# Produce baseline true value silhouette scores
sil_score_eucl = silhouette_score(X_scaled, kmeans_labels, metric="euclidean")
sil_score_manhat = silhouette_score(X_scaled, kmeans_labels, metric="manhattan")

print("Euclidean Silhouette Score: ", round(sil_score_eucl, 4))
print("Manhattan Silhouette Score: ", round(sil_score_manhat, 4))


#DBSCAN Method
X_numeric = data[scaled_cols]
X_scaled = RobustScaler().fit_transform(X_numeric)

# from sklearn.decomposition import PCA

# pca = PCA(n_components=5)
# X_scaled = pca.fit_transform(X_scaled)

possible_eps_values = np.linspace(start=0.1, stop=15, num=100)

eps_values_eucl = []
eps_values_man = []
dbscan_eucl_sil_values = []
dbscan_man_sil_values = []

for reach_dist in possible_eps_values:
    
    dbscan_eucl = DBSCAN(eps=reach_dist, metric="euclidean", min_samples=20).fit(X_scaled)
    labels_pred_eucl = dbscan_eucl.labels_

    dbscan_man = DBSCAN(eps=reach_dist, metric="manhattan", min_samples=20).fit(X_scaled)
    labels_pred_man = dbscan_man.labels_

    if len(np.unique(labels_pred_eucl)) > 1:
        eucl_sil_score = silhouette_score(X_scaled, labels_pred_eucl, metric="euclidean")
        eps_values_eucl.append(reach_dist)
        dbscan_eucl_sil_values.append(eucl_sil_score)
    
    if len(np.unique(labels_pred_man)) > 1:
        man_sil_score = silhouette_score(X_scaled, labels_pred_man, metric="manhattan")
        eps_values_man.append(reach_dist)
        dbscan_man_sil_values.append(man_sil_score)

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
dbscan_eucl.fit(X_scaled)

data['Group (dbscan eucl)'] = dbscan_eucl.labels_
dbscan_labels = dbscan_eucl.labels_

class0_eucl = data[data['Group (dbscan eucl)']==0]
class1_eucl = data[data['Group (dbscan eucl)']==1]
class2_eucl = data[data['Group (dbscan eucl)']==2]
class3_eucl = data[data['Group (dbscan eucl)']==-1]

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)
plt.scatter(class0_eucl['Number 5s Scored'], class0_eucl['Score'], label = 'class 0')
plt.scatter(class1_eucl['Number 5s Scored'], class1_eucl['Score'], label = 'class 1')
plt.scatter(class2_eucl['Number 5s Scored'], class2_eucl['Score'], label = 'class 2')
plt.scatter(class3_eucl['Number 5s Scored'], class3_eucl['Score'], label = 'class 3')

plt.legend(fontsize = 15)
plt.title('Comparing DBSCAN clusters for Total Score against Number of 5s Scored \n with "Euclidean" Method', fontsize = 22)
plt.xlabel("Number of 5s Scored", fontsize = 16)
plt.ylabel("Total Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


dbscan_man = DBSCAN(eps=man_eps_max, metric="manhattan", min_samples=20)
dbscan_man.fit(X_scaled)

data['Group (dbscan man)'] = dbscan_man.labels_
dbscan_labels = dbscan_man.labels_

class0_man = data[data['Group (dbscan man)']==0]
class1_man = data[data['Group (dbscan man)']==1]
class2_man = data[data['Group (dbscan man)']==2]
class3_man = data[data['Group (dbscan man)']==-1]

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)
plt.scatter(class0_man['Number 5s Scored'], class0_man['Score'], label = 'class 0')
plt.scatter(class1_man['Number 5s Scored'], class1_man['Score'], label = 'class 1')
plt.scatter(class2_man['Number 5s Scored'], class2_man['Score'], label = 'class 2')
plt.scatter(class3_man['Number 5s Scored'], class3_man['Score'], label = 'class 3')

plt.legend(fontsize = 15)
plt.title('Comparing DBSCAN clusters for Total Score against Number of 5s Scored \n with "Manhattan" Method', fontsize = 22)
plt.xlabel("Number of 5s Scored", fontsize = 16)
plt.ylabel("Total Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()
