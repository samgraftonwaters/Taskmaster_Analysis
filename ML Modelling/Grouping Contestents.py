from sklearn.cluster import KMeans
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
# from Correlations.Correlation_Functions import Correlation_Functions as CF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(model_data.head())

print(model_data.info())

print(model_data.columns)

data = model_data.drop(['Series', 'Name'], axis = 1)

data = pd.DataFrame(data)

data_nums = data.select_dtypes(include=[float, int])

correlations = data_nums.corr(method = 'spearman')
grouped_variables = CF.group_corr_variables(correlations = correlations)
print('Correlation > 0.7:')
print(CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.7))
print('\nCorrelation > 0.9:')
print(CF.set_corr_thresholds(corr_data = grouped_variables, range = False, threshold = 0.9))

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

X_scaled = preprocessor.fit_transform(data)

# ---- Run KMeans ----
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
kmeans.fit(X_scaled)

data['Group'] = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

feature_names = scaled_cols + ohe_cols + cat_cols
centers_df = pd.DataFrame(centers_scaled, columns=feature_names)

scaler = preprocessor.named_transformers_['num']
centers_df[scaled_cols] = scaler.inverse_transform(centers_df[scaled_cols])

print(centers_df)
print(centers_df.iloc[[0]])
# print(centers_df.iloc[[2]])

class0 = data[data['Group']==0]
class1 = data[data['Group']==1]
class2 = data[data['Group']==2]


fig = plt.subplots(figsize = (10, 8))
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
plt.xlabel("Number of 5s Scored")
plt.ylabel("Total Score")
plt.show()



fig = plt.subplots(figsize = (10, 8))
plt.scatter(class0['Tie Breaks per series'], class0['Episode Percentage Lossses'], label = 'class 0')
plt.scatter(class1['Tie Breaks per series'], class1['Episode Percentage Lossses'], label = 'class 1')
plt.scatter(class2['Tie Breaks per series'], class2['Episode Percentage Lossses'], label = 'class 2')

plt.scatter(centers_df.iloc[[0]]['Tie Breaks per series'], centers_df.iloc[[0]]['Episode Percentage Lossses'], marker ='*', 
            s = 300, color='blue')
plt.scatter(centers_df.iloc[[1]]['Tie Breaks per series'], centers_df.iloc[[1]]['Episode Percentage Lossses'], marker ='*', 
            s = 300, color='darkorange')
plt.scatter(centers_df.iloc[[2]]['Tie Breaks per series'], centers_df.iloc[[2]]['Episode Percentage Lossses'], marker ='*', 
            s = 300, color='green')

plt.legend(fontsize = 15)
plt.xlabel('Tie Breaks per series')
plt.ylabel('Episode Percentage Lossses')
plt.show()


cluster_labels = kmeans.fit_predict(X_scaled)


# Produce baseline true value silhouette scores
sil_score_eucl = silhouette_score(X_scaled, cluster_labels , metric="euclidean")
sil_score_manhat = silhouette_score(X_scaled, cluster_labels , metric="manhattan")

print("Euclidean Silhouette Score: ", round(sil_score_eucl, 4))
print("Manhattan Silhouette Score: ", round(sil_score_manhat, 4))

k_values = list(range(2, 10))

sil_values = []

for k in k_values:
    # Perform the clustering for a given value of K
    km_clusterer = KMeans(n_clusters=k, init="random", 
                          max_iter=5, random_state=123)
    
    labels_pred = km_clusterer.fit_predict(X_scaled)
    # Calculate the silhouette score for associated k clusters
    eucl_sil_score = silhouette_score(X_scaled, labels_pred, metric="euclidean")
    # Add the score the list of scores
    sil_values.append(eucl_sil_score)


fig, ax = plt.subplots(figsize=(6,4))

plt.plot(k_values, sil_values, c="darkgreen")
plt.hlines(sil_score_eucl, 0, 11, lw=3)
plt.hlines(sil_score_manhat,0, 11, lw=3)

ax.set_title("Silhouette Score for different K")
ax.set_xlabel("K")
ax.set_ylabel("Euclidean Silhoette Score")
plt.show()


#Inertias

inertias = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.show()

#Calinski–Harabasz Index

scores = []

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X_scaled)
    score = calinski_harabasz_score(X_scaled, labels)
    scores.append(score)

plt.plot(range(2, 11), scores, marker='o')
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.show()


def evaluate_kmeans(k):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X_scaled)
    return silhouette_score(X_scaled, labels)

best_k = max(range(2, 11), key=evaluate_kmeans)

print("Best k:", best_k)

# params = {
#     'n_clusters': range(2, 10),
#     'init': ['k-means++', 'random'],
#     'n_init': [0, 5, 10, 15],
#     'max_iter': [100, 200, 300, 400, 500],
#     'tol': [0.0001, 0.001, 0.01],
#     'algorithm': ['lloyd', 'elkan'],
# }

# # Create the KMeans object
# kmeans = KMeans(random_state=42)

# # Perform grid search
# grid_search = GridSearchCV(kmeans, param_grid=params, cv=5)

# # Fit the grid search to the data
# grid_search.fit(X_scaled)

# # Print the best hyperparameters
# print("Best hyperparameters: ", grid_search.best_params_)
# print('Optimal number of clusters based on parameter grid: ' + str(grid_search.best_params_['n_clusters']))

# silhouette = silhouette_score(X_scaled, grid_search.labels_)