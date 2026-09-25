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

#Selecting only Numerical Data
data_nums = data.select_dtypes(include=[float, int])

print(data_nums.columns)

data_nums = data_nums.drop(columns = ['Score', 'Avg_Score_per_Episodes', 'Team_Score_per_Person',
                                      'Number_Episodes', 'Number_of_Tasks'],  axis = 1)

# ['Position', 'Score', 'Disqualifications', 'Episode_Percentage_Losses',
#        'Number_of_Tasks', 'Percent_1s_Scored', 'Tie_Break_Losses',
#        'Tie_Break_Wins', 'Tie_Breaks_per_series', 'Avg_Score_per_Episodes',
#        'Avg_Score_per_Tasks', 'Episode_Percentage_Wins', 'Number_Episodes',
#        'Number_Team_Tasks', 'Percent_5s_Scored', 'Series_Number',
#        'Team_Score_per_Task', 'Team_Score_per_Person', 'Team_A', 'Team_B',
#        'Age_Ranges_20-29', 'Age_Ranges_30-39', 'Age_Ranges_40-49',
#        'Age_Ranges_50-59', 'Age_Ranges_60-69', 'Gender_Female', 'Gender_Male',
#        'Gender_Non-Binary', 'Seat_Seat_1', 'Seat_Seat_2', 'Seat_Seat_3',
#        'Seat_Seat_4', 'Seat_Seat_5']

# # PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(data_nums)

cluster_data["PCA1"] = X_pca[:,0]
cluster_data["PCA2"] = X_pca[:,1]

k_values = range(2, 12)

print()
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
    sil_max_K_value_kmeans = max(zip(k_values, sil_values_kmeans_eucl), key=lambda x: x[1])[0]
    highest_sil_value_kmeans = max(sil_values_kmeans_eucl)
    print("Best Euclidean Sillhouette Score:", round(highest_sil_value_kmeans, 4))
    print("Best Euclidean K:", sil_max_K_value_kmeans)

else:
    kmeans_distance_method = 'manhattan'
    sil_max_K_value_kmeans = max(zip(k_values, sil_values_kmeans_man), key=lambda x: x[1])[0]
    highest_sil_value_kmeans = max(sil_values_kmeans_man)
    print("Best Manhattan Sillhouette Score:", round(highest_sil_value_kmeans, 4))
    print("Best Manhattan K:", sil_max_K_value_kmeans)


# ---- Run KMeans ----
kmeans = KMeans(n_clusters=sil_max_K_value_kmeans)
kmeans.fit(X_pca)

cluster_data[f'Group (kmeans {kmeans_distance_method})'] = kmeans.labels_
kmeans_labels = kmeans.labels_
centers_scaled = kmeans.cluster_centers_

print(centers_scaled)

groups_kmeans = np.unique(kmeans.labels_)
print(groups_kmeans)

feature_names = ['PCA1', 'PCA2']
centers_df = pd.DataFrame(centers_scaled, columns=feature_names)
print(centers_df)

colours = plt.cm.tab10.colors

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_kmeans, colours):
    plt.scatter(cluster_data[cluster_data[f'Group (kmeans {kmeans_distance_method})']==group]['PCA1'], 
                cluster_data[cluster_data[f'Group (kmeans {kmeans_distance_method})']==group]['PCA2'], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

    plt.scatter(centers_df.iloc[[group]]['PCA1'], centers_df.iloc[[group]]['PCA2'], 
                marker ='*', s = 450, color=colour, edgecolor = 'black',
                label = f'Class {group} Center')

plt.legend(fontsize = 15, ncols = 2)
plt.title(f'Comparing Kmeans clusters using the {kmeans_distance_method} distance method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

print()
#####
#2. DBSCAN Method
#####
print('DBSCAN Method')

possible_eps_values = np.linspace(start=0.1, stop=15, num=100)

dbscan_eucl_sil_values, eps_values_eucl = GCF.get_dbscan_silhouette_epsilon_values(X_data = X_pca, epsilon_range = possible_eps_values, distance_method = 'euclidean')
dbscan_man_sil_values, eps_values_man = GCF.get_dbscan_silhouette_epsilon_values(X_data = X_pca, epsilon_range = possible_eps_values, distance_method = 'manhattan')

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.98)
plt.plot(eps_values_eucl, dbscan_eucl_sil_values, c="blueviolet", marker = 'o', label = 'Euclidean', 
         lw = 3, markersize = 12)
plt.plot(eps_values_man, dbscan_man_sil_values, c="dodgerblue", marker = 'o', label = 'Manhattan', 
         lw = 3, markersize = 12)
plt.title("Silhouette Score for different Reach Distances", fontsize = 22)
plt.xlabel(r"Reach Distance ($\epsilon$)", fontsize = 16)
plt.ylabel("Silhoette Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 16)
plt.show()


if max(dbscan_eucl_sil_values) > max(dbscan_man_sil_values):
    dbscan_distance_method = 'euclidean'
    eps_max_dbscan = max(zip(eps_values_eucl, dbscan_eucl_sil_values), key=lambda x: x[1])[0]
    dbscan_highest_sil_values = max(dbscan_eucl_sil_values)
    print("Best Euclidean Silhouette Score: ", round(dbscan_highest_sil_values, 4))
    print(r"Best Euclidean Reach Distance ($\epsilon$)", eps_max_dbscan)

else:
    dbscan_distance_method = 'Manhattan'
    eps_max_dbscan = max(zip(eps_values_man, dbscan_man_sil_values), key=lambda x: x[1])[0]
    dbscan_highest_sil_values = max(dbscan_man_sil_values)
    print("Best Manhattan Silhouette Score: ", round(dbscan_highest_sil_values, 4))
    print(r"Best Manhattan Reach Distance ($\epsilon$)", eps_max_dbscan)

#-----Run DBSCAN-----

dbscan = DBSCAN(eps=eps_max_dbscan, metric=dbscan_distance_method)
dbscan.fit(X_pca)

cluster_data[f'Group (dbscan {dbscan_distance_method})'] = dbscan.labels_
dbscan_labels = dbscan.labels_
groups_dbscan = np.unique(dbscan_labels)
print(groups_dbscan)

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_dbscan, colours):
    
    plt.scatter(cluster_data[cluster_data[f'Group (dbscan {dbscan_distance_method})']==group]['PCA1'], 
                cluster_data[cluster_data[f'Group (dbscan {dbscan_distance_method})']==group]['PCA2'], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

plt.legend(fontsize = 15)
plt.title(f'Comparing DBSCAN clusters with {dbscan_distance_method} distance method', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

print()

#######
#3.Hierarchical Clustering
########
print('Hierarchical Clustering Method')

#Create model for each linkage method

single = GCF.determine_sil_values_agg_both_distance_methods(k_range = k_values, X_data = X_pca, link_type = 'single')
complete = GCF.determine_sil_values_agg_both_distance_methods(k_range = k_values, X_data = X_pca, link_type = 'complete')
average = GCF.determine_sil_values_agg_both_distance_methods(k_range = k_values, X_data = X_pca, link_type = 'average')
ward = GCF.determine_sil_values_agg_both_distance_methods(k_range = k_values, X_data = X_pca, link_type = 'ward')

cluster_method = ['single', 'complete', 'average', 'ward']

###Euclidean method
eucl_agg_sil_values = []
eucl_max_k_agg = []
eucl_max_sil_agg = []

for cluster in cluster_method:
    eucl_agg = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = cluster, 
                                 distance_method = 'euclidean')
    k_agg_max = max(zip(k_values, eucl_agg), key=lambda x: x[1])[0]
    sil_agg_max = max(eucl_agg)
    eucl_agg_sil_values.append(eucl_agg)
    eucl_max_k_agg.append(k_agg_max)
    eucl_max_sil_agg.append(sil_agg_max)


highest_eucl_sil_value = max(eucl_max_sil_agg)
max_index_eucl = eucl_max_sil_agg.index(max(eucl_max_sil_agg))
highest_eucl_k_value = eucl_max_k_agg[max_index_eucl]
best_eucl_agg_cluster = cluster_method[max_index_eucl]

###Manhattan method
man_agg_sil_values = []
man_max_k_agg = []
man_max_sil_agg = []

for cluster in cluster_method[0:3]:
    man_agg = GCF.determine_sil_values_agg(k_range = k_values, X_data = X_pca, link_type = cluster, 
                                 distance_method = 'manhattan')
    k_agg_max = max(zip(k_values, man_agg), key=lambda x: x[1])[0]
    sil_agg_max = max(man_agg)
    man_agg_sil_values.append(man_agg)
    man_max_k_agg.append(k_agg_max)
    man_max_sil_agg.append(sil_agg_max)

highest_man_sil_value = max(man_max_sil_agg)
max_index_man = man_max_sil_agg.index(max(man_max_sil_agg))
highest_man_k_value = man_max_k_agg[max_index_man]
best_man_agg_cluster = cluster_method[max_index_man]

###Plotting
# colours = ["darkgreen", "dodgerblue", "blueviolet", "darkorange"]

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.98)

for sil_values, cluster, colour in zip(eucl_agg_sil_values, cluster_method, colours):
    plt.plot(k_values, sil_values, c=colour, marker='o', label = cluster,
             lw = 3, markersize = 12)

plt.title("Hierarchical Clustering Silhouette Scores for different \n K using the Euclidean distance method", fontsize = 22)
plt.xlabel("Number of Clusters (K)", fontsize = 16)
plt.ylabel("Silhoette Score (Euclidean)", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 16)
plt.show()

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.98)

for sil_values, cluster, colour in zip(man_agg_sil_values, cluster_method[0:3], colours):
    plt.plot(k_values, sil_values, c=colour, marker='o', label = cluster,
             lw = 3, markersize = 12)

plt.title("Hierarchical Clustering Silhouette Scores for different \n K using the Manhattan distance method", fontsize = 22)
plt.xlabel("Number of Clusters (K)", fontsize = 16)
plt.ylabel("Silhoette Score (Manhattan)", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 16)
plt.show()

#Determine best agg method

if highest_eucl_sil_value > highest_man_sil_value:
    agg_distance_method = 'euclidean'
    highest_k_value_agg = highest_eucl_k_value
    agg_cluster_method = best_eucl_agg_cluster
    highest_sil_value_agg = highest_eucl_sil_value
    print("Best Euclidean Silhouette Score: ", round(highest_sil_value_agg, 4))
    print("Best Euclidean K: ", highest_k_value_agg)
    print("Best Euclidean Agg Method: ", agg_cluster_method)

else:
    agg_distance_method = 'manhattan'
    highest_k_value_agg = highest_man_k_value
    agg_cluster_method = best_man_agg_cluster
    highest_sil_value_agg = highest_eucl_sil_value
    print("Best Manhattan Silhouette Score: ", round(highest_sil_value_agg, 4))
    print("Best Manhattan K:", highest_k_value_agg)
    print("Best Manhattan Agg Method: ", agg_cluster_method)


agg_model = AgglomerativeClustering(n_clusters=highest_k_value_agg, linkage=agg_cluster_method, 
                                    metric = agg_distance_method).fit(X_pca)

#Access labels assigned for each method
agg_labels = agg_model.labels_
cluster_data[f'Group (Agg {agg_distance_method} {agg_cluster_method})'] = agg_labels
groups_agg = np.unique(agg_labels)
print(groups_agg)

centers = cluster_data.groupby(f'Group (Agg {agg_distance_method} {agg_cluster_method})')[["PCA1","PCA2"]].mean()

fig, ax = plt.subplots()
plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.07, right = 0.98)

for group, colour in zip(groups_agg, colours):
    
    plt.scatter(cluster_data[cluster_data[f'Group (Agg {agg_distance_method} {agg_cluster_method})']==group]['PCA1'], 
                cluster_data[cluster_data[f'Group (Agg {agg_distance_method} {agg_cluster_method})']==group]['PCA2'], 
                label = f'Class {group}', color = colour, marker = 'o', s = 50)

    plt.scatter(centers.iloc[[group]]["PCA1"], centers.iloc[[group]]["PCA2"], 
            marker ='*', s = 450, color=colour, edgecolor = 'black',
            label = f'Class {group} Center')
    
plt.legend(fontsize = 15, ncols = 2)
plt.title(f'Comparing Agglomerative clusters with {agg_distance_method} distance \n method and {agg_cluster_method} Linkage', fontsize = 22)
plt.xlabel("PCA1", fontsize = 16)
plt.ylabel("PCA2", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


### Combinng all model parameters together
cluster_model_parameters = pd.DataFrame({
    "Cluster Model" : ['Kmeans', 'DBSCAN', 'Agglomerative'],
    "Number of Clusters" : [len(groups_kmeans), len(groups_dbscan), len(groups_agg)],
    "Cluster Values" : [groups_kmeans, groups_dbscan, groups_agg],
    "Silhouette Score" : [highest_sil_value_kmeans, dbscan_highest_sil_values, highest_sil_value_agg],
    "Main Model Parameter" : [int(sil_max_K_value_kmeans), float(eps_max_dbscan), int(highest_k_value_agg)],
    "Distance Method" : [kmeans_distance_method, dbscan_distance_method, agg_distance_method],
    "Link Type" : [None, None, agg_cluster_method],
    "Cluster Column" : [f'Group (kmeans {kmeans_distance_method})',
                        f'Group (dbscan {dbscan_distance_method})', 
                        f'Group (Agg {agg_distance_method} {agg_cluster_method})']
 

})

filtered = cluster_model_parameters[cluster_model_parameters['Number of Clusters'] >= 1]

best_cluster_model = filtered.loc[filtered['Silhouette Score'].idxmax()]

cluster_data_grouped = cluster_data[['Series', 'Name', 'PCA1', 'PCA2', 
                                     best_cluster_model['Cluster Column']]]


#Read in some other data to determine what each group means

positions = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')
overall_rank = pd.read_csv(file_path + 'Overall Contestent Performance.csv')

positions = positions[['Name','Score','Position']]
overall_rank = overall_rank[['Name', 'final_score_rescale', 'Contestent Rank']]

# cluster_data_grouped = cluster_data_grouped.merge(pd.merge(positions, data_nums, on = 'Name', 
#                                                            how = 'left'), 
#                                                            on = 'Name', how = 'left')

cluster_data_grouped = pd.concat([cluster_data_grouped, positions['Score'], data_nums], axis = 1)                                                    
print(cluster_data_grouped.head())
print(cluster_data_grouped.columns)

different_groups = []
# grouped_details = []

for i, group in enumerate(best_cluster_model["Cluster Values"]):
    cluster_group = cluster_data_grouped[cluster_data_grouped[best_cluster_model['Cluster Column']] == group].reset_index(drop = True)
    different_groups.append(cluster_group)
    print(f'\nGroup {i}')
    print(cluster_group.head())
    print(len(cluster_group))
    
#     for col in ['Score', 'Position', 'Team_Score_per_Task', 'Avg_Score_per_Tasks']:#'final_score_rescale', 'Contestent Rank']:

#         median_value = round(different_groups[i][col].median(), 2)
#         average_value = round(different_groups[i][col].mean(), 2)

#         average_median_groups = {
#             "Group": i,
#             "Metric" : col,
#             f"Average": average_value,
#             f"Median": median_value
#         }

#         grouped_details.append(average_median_groups)

#     print()

# grouped_details_df = pd.DataFrame(grouped_details)

# print(grouped_details_df)

# GCF.plot_bar_groups(dataframe = grouped_details_df, average_metric = 'Average', 
#                     columns = ['Score', 'Position', 'Team_Score_per_Task', 'Avg_Score_per_Tasks'])
# GCF.plot_bar_groups(dataframe = grouped_details_df, average_metric = 'Median',
#                     columns = ['Score', 'Position', 'Team_Score_per_Task', 'Avg_Score_per_Tasks'])

# print(best_cluster_model)

#Save final data tables

cluster_data_grouped.to_csv(file_path + 'Final Cluster Model Grouped Contestents.csv', sep = ',', index = False)

cluster_model_parameters.to_csv(file_path + 'Clustering Model Parameters.csv', sep = ',', index = False)

with pd.ExcelWriter(file_path + 'Different Cluster Groups.xlsx') as writer:
    for group in best_cluster_model["Cluster Values"]:
        df = different_groups[group]  

        df.to_excel(writer, sheet_name = f'Group {group}', index = False)
