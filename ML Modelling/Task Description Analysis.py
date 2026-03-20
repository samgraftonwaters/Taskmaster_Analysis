import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import Task_Text_Cleaning_Functions as TTCF
import Grouping_Contestent_Functions as GCF


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

k_values = range(2, 30)

def full_task_theme_analysis(cleaned_task_text, theme_type, output_file_name):

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleaned_task_text)

    sil_scores_eucl = GCF.determine_kmeans_sil_values(k_range = k_values, X_data = X, distance_method = 'euclidean')

    GCF.plot_clustering_line_graphs(x_values = k_values , y_values = sil_scores_eucl, 
                                    labels = f'{theme_type} Task Descriptions', colours = 'blue', 
                                    title = f'Silhouette Score against Clusters (K) for {theme_type} Task Descriptions', 
                                    y_label = 'Silhouette Score', x_label = 'K')

    max_k = max(zip(k_values, sil_scores_eucl), key=lambda x: x[1])[0]
    max_sil = max(sil_scores_eucl)

    print("Max K: ", max_k)
    print("Max Silhouette: ", max_sil)

    task_clusters = TTCF.task_theme_clusters_kmeans(max_k = max_k, X_data = X, cleaned_tasks_description = cleaned_tasks)

    TTCF.save_task_themes(task_clusters, theme_type = theme_type, file_name = output_file_name, 
                        file_path = file_path)
    
####### All Tasks

task_description = task_data['Description'].copy()

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'All', 
                         output_file_name = 'All_Task_Descriptions')




