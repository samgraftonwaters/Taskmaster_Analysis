import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import Task_Text_Cleaning_Functions as TTCF
import Grouping_Contestent_Functions as GCF


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

k_values = range(2, 30)

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)



vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_tasks)



sil_scores_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X, distance_method = 'euclidean')

GCF.plot_clustering_line_graphs(x_values = k_values , y_values = sil_scores_eucl, 
                                labels = 'kmeans', colours = 'blue', title = '', y_label = 'SS', x_label = 'K')

max_k = max(zip(k_values, sil_scores_eucl), key=lambda x: x[1])[0]
max_sil = max(sil_scores_eucl)

print(max_k)
print(max_sil)

task_clusters = TTCF.task_theme_clusters_kmeans(max_k = max_k, X_data = X, cleaned_tasks_description = cleaned_tasks)

TTCF.save_task_themes(task_clusters, theme_type = 'All', file_name = 'All_Task_Descriptions', 
                      file_path = file_path)
# results = []

# for i in range(5):
#     results.append(f"Number: {i}")

# with open("output.txt", "w") as f:
#     f.write("\n".join(results))
######
# with open("output.txt", "w") as f:
#     for i in range(5):
#         f.write(f"Number: {i}\n")
######
# with open("output.txt", "w") as f:
#     for i in range(5):
#         print(f"Number: {i}", file=f)