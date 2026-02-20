from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(model_data.head())

print(model_data.info())

print(model_data.columns)

data = model_data.drop(['Series', 'Name'], axis = 1)

data = pd.DataFrame(data)

scaled_cols = ['Score', 'Position', 'Avg Score per Episodes',
       'Avg Score per Tasks', 'Number 5s Scored', 'Number 1s Scored',
       'Tie Break Wins', 'Tie Break Losses', 'Tie Breaks per Person',
       'Tie Breaks per series', 'Disqualifications', 'Number_Episodes',
       'Episode Percentage Wins', 'Episode Percentage Lossses',
       'Number Team Tasks', 'Team Total', 'Team Score per Person Task']

ohe_cols = [ 'Team_A', 'Team_B', 'Age_Ranges_20 - 29', 'Age_Ranges_30 - 39',
       'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 'Age_Ranges_60 - 69',
       'Gender_Female', 'Gender_Male', 'Gender_Non-Binary', 'Seat_Seat 1',
       'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', RobustScaler(), scaled_cols),
        ('ohe', 'passthrough', ohe_cols)
    ]
)

X_scaled = preprocessor.fit_transform(data)

# ---- Run KMeans ----
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
kmeans.fit(X_scaled)

data['Group'] = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

feature_names = scaled_cols + ohe_cols
centers_df = pd.DataFrame(centers_scaled, columns=feature_names)

scaler = preprocessor.named_transformers_['num']
centers_df[scaled_cols] = scaler.inverse_transform(centers_df[scaled_cols])

print(centers_df)
print(centers_df.iloc[[0]])
print(centers_df.iloc[[2]])

class0 = data[data['Group']==0]
class1 = data[data['Group']==1]
class2 = data[data['Group']==2]


fig = plt.subplots(figsize = (10, 8))
plt.scatter(class0['Number 5s Scored'], class0['Score'], label = 'class 0')
plt.scatter(class1['Number 5s Scored'], class1['Score'], label = 'class 1')
plt.scatter(class2['Number 5s Scored'], class2['Score'], label = 'class 2')
#plt.scatter(cricket_data['Number 5s Scored'], cricket_data['score'], c=kmeans_fit_all, label = 'class 0')

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




# Produce baseline true value silhouette scores
sil_score_eucl = silhouette_score(X_scaled, data['Group'], metric="euclidean")
sil_score_manhat = silhouette_score(X_scaled, data['Group'], metric="manhattan")

print("Euclidean Silhouette Score: ", round(sil_score_eucl, 4))
print("Manhattan Silhouette Score: ", round(sil_score_manhat, 4))

k_values = list(range(2, 10))

sil_values = []

for k in k_values:
    # Perform the clustering for a given value of K
    km_clusterer = KMeans(n_clusters=k, init="random", 
                          max_iter=5, random_state=123).fit(X_scaled)
    
    labels_pred = km_clusterer.labels_
    # Calculate the silhouette score for associated k clusters
    eucl_sil_score = silhouette_score(X_scaled, labels_pred, metric="euclidean")
    # Add the score the list of scores
    sil_values.append(eucl_sil_score)


fig, ax = plt.subplots(figsize=(6,4))

plt.plot(k_values, sil_values, c="darkgreen")

ax.set_title("Silhouette Score for different K")
ax.set_xlabel("K")
ax.set_ylabel("Euclidean Silhoette Score")
plt.show()


