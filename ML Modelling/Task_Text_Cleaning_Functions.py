import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import spacy
from sklearn.cluster import KMeans

nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))
task_words = ['prize', 'live', 'team']
lemmatizer = WordNetLemmatizer()

def clean_task_description(task_description_text):

    """
    
    """

    task_description = task_description_text.copy()

    task_description = task_description.str.lower()

    task_description = task_description.apply(nltk.word_tokenize)

    task_description = task_description.apply(lambda x: [w for w in x if w.isalpha()])

    task_description = task_description.apply(lambda x: [w for w in x if w not in stop_words and w not in task_words])

    task_description = task_description.apply(lambda x: [w for w in x if len(w) > 2])

    task_description = task_description.apply(lambda x: [lemmatizer.lemmatize(w) for w in x])

    task_description = task_description.apply(lambda x: " ".join(x))

    return(task_description)

def task_theme_clusters_kmeans(max_k, X_data, cleaned_tasks_description):
    kmeans = KMeans(n_clusters=max_k, random_state=42, n_init=10)
    kmeans.fit(X_data)

    clusters = kmeans.labels_

    clustered_tasks = {}
    for i, label in enumerate(clusters):
        clustered_tasks.setdefault(label, []).append(cleaned_tasks_description.iloc[i])

    return(clustered_tasks)

def save_task_themes(task_clusters, theme_type:str, file_name:str, file_path:str, descriptions):
    with open(file_path + file_name + ".txt", "w") as f:
        print(theme_type, f"\nNumber of Themes = {len(task_clusters)}", f"\nNumber of Task Descriptions = {len(descriptions)}\n", file = f)
        for cluster_id, task_list in task_clusters.items():
            print(f"\n{theme_type} Theme {cluster_id+1} (example tasks):", file = f)
            for t in task_list[:5]:
                print("-", t, file = f)
