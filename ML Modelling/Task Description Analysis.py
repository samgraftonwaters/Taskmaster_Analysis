import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import Task_Text_Cleaning_Functions as TTCF
import Grouping_Contestent_Functions as GCF
plt.rcParams['figure.figsize'] = (13, 7)


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Only.csv')

k_values = range(2, 30)

def full_task_theme_analysis(cleaned_task_text, theme_type, output_file_name, k_range):

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleaned_task_text)

    sil_scores_eucl = GCF.determine_kmeans_sil_values(k_range = k_range, X_data = X, distance_method = 'euclidean')

    GCF.plot_clustering_line_graphs(x_values = k_range , y_values = sil_scores_eucl, 
                                    labels = f'{theme_type} Task Descriptions', colours = 'blue', 
                                    title = f'Silhouette Score against Clusters (K) for {theme_type} Task Descriptions', 
                                    y_label = 'Silhouette Score', x_label = 'K')

    max_k = max(zip(k_values, sil_scores_eucl), key=lambda x: x[1])[0]
    max_sil = max(sil_scores_eucl)

    print(f"{theme_type}:\n")
    print("Number of Task Descriptions:", len(cleaned_task_text))
    print("Max K: ", max_k)
    print("Max Silhouette: ", round(max_sil, 4))
    print()

    task_clusters = TTCF.task_theme_clusters_kmeans(max_k = max_k, X_data = X, 
                                                    cleaned_tasks_description = cleaned_task_text)

    TTCF.save_task_themes(task_clusters, theme_type = theme_type, file_name = output_file_name, 
                        file_path = file_path, descriptions = cleaned_task_text)

    return(k_values, sil_scores_eucl)
    
####### All Tasks

task_description = task_data['Description'].copy()

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

all_k, all_sil = full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'All', 
                         output_file_name = 'All_Task_Descriptions', k_range = k_values)


###### Prize Tasks

task_description = task_data[task_data['Prize Task'] == 1]['Description']

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

prize_k, prize_sil = full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'Prize', 
                         output_file_name = 'Prize_Task_Descriptions', k_range = k_values)



###### Team Tasks

task_description = task_data[task_data['Team Task'] == 1]['Description']

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

team_k, team_sil = full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'Team', 
                         output_file_name = 'Team_Task_Descriptions', k_range = k_values)


###### Live Tasks

task_description = task_data[task_data['Live Task'] == 1]['Description']

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

live_k, live_sil = full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'Live', 
                         output_file_name = 'Live_Task_Descriptions', k_range = k_values)

###### Normal Tasks

task_description = task_data[(task_data['Team Task'] != 1) & (task_data['Prize Task'] != 1) & (task_data['Live Task'] != 1)]['Description'].copy()

cleaned_tasks = TTCF.clean_task_description(task_description_text = task_description)

normal_k, normal_sil = full_task_theme_analysis(cleaned_task_text = cleaned_tasks, theme_type = 'Normal', 
                         output_file_name = 'Normal_Task_Descriptions', k_range = k_values)

####
colours = plt.cm.tab10.colors

GCF.plot_clustering_line_graphs(x_values = [all_k, prize_k, team_k, live_k, normal_k], 
                                y_values = [all_sil, prize_sil, team_sil, live_sil, normal_sil], 
                                labels = ['All Task Descriptions','Prize Task Descriptions','Team Task Descriptions',
                                          'Live Task Descriptions', 'Normal Task Descriptions'],
                                colours = [colours[0], colours[1], colours[2], colours[3], colours[4]],
                                title = f'Silhouette Score against Clusters (K) for different Task Descriptions', 
                                y_label = 'Silhouette Score', x_label = 'K')