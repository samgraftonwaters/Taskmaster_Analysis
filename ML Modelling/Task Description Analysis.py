import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import Text_Cleaning as TC
import Grouping_Contestent_Functions as GCF


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())

cleaned_tasks = TC.clean_task_description(task_description_text = task_description)

print(cleaned_tasks)
print(len(cleaned_tasks))

# Step 1: Convert tasks to numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_tasks)

k_values = range(2, 30)

sil_scores_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X, distance_method = 'euclidean')

GCF.plot_clustering_line_graphs(x_values = k_values , y_values = sil_scores_eucl, 
                                labels = 'kmeans', colours = 'blue', title = '', y_label = 'SS', x_label = 'K')

max_k = max(zip(k_values, sil_scores_eucl), key=lambda x: x[1])[0]
max_sil = max(sil_scores_eucl)

print(max_k)
print(max_sil)

# Step 2: Cluster tasks into 20 themes
kmeans = KMeans(n_clusters=max_k, random_state=42, n_init=10)
kmeans.fit(X)

# Step 3: Assign tasks to clusters
clusters = kmeans.labels_

# Step 4: Collect representative task from each cluster
clustered_tasks = {}
for i, label in enumerate(clusters):
    clustered_tasks.setdefault(label, []).append(cleaned_tasks[i])

# Step 5: Print short outputs for each cluster (max 5 tasks each)
for cluster_id, task_list in clustered_tasks.items():
    print(f"\nTheme {cluster_id+1} (example tasks):")
    for t in task_list[:5]:
        print("-", t)
