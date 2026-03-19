import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import Text_Cleaning as TC


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

# Step 2: Cluster tasks into 20 themes
num_clusters = 10
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
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
