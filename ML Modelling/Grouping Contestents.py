from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np

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
centers = kmeans.cluster_centers_
print(centers)

print(data)

class0 = data[data['Group']==0]
class1 = data[data['Group']==1]
class2 = data[data['Group']==2]


fig = plt.subplots(figsize = (10, 8))
plt.scatter(class0['runs_scored'], class0['average'], label = 'class 0')
plt.scatter(class1['runs_scored'], class1['average'], label = 'class 1')
plt.scatter(class2['runs_scored'], class2['average'], label = 'class 2')
#plt.scatter(cricket_data['runs_scored'], cricket_data['average'], c=kmeans_fit_all, label = 'class 0')

plt.scatter(kmeans_analysis_all.cluster_centers_[:,5],kmeans_analysis_all.cluster_centers_[:,3], 
            marker ='*',color='black')

plt.legend(fontsize = 15)
plt.xlabel("Runs Scored")
plt.ylabel("Batting Average")
plt.show()



