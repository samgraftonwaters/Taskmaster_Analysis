import pandas as pd
import Text_Cleaning as TC

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.system("pip install sentence-transformers==2.2.2 transformers<4.40 bertopic<0.16")

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())

cleaned_tasks = TC.clean_task_description(task_description_text = task_description)

print(cleaned_tasks)
print(len(cleaned_tasks))

print('BERT')
from bertopic import BERTopic

topic_model = BERTopic(min_topic_size=3)
topics, probs = topic_model.fit_transform(cleaned_tasks)

topic_model.get_topic_info()

info = topic_model.get_topic_info()
print(info)

for topic_id in topic_model.get_topics():
    if topic_id == -1:
        continue  # skip outliers
    
    print(f"\nTopic {topic_id}:")
    print(topic_model.get_topic(topic_id))

from collections import defaultdict

topic_docs = defaultdict(list)

for doc, topic in zip(cleaned_tasks, topics):
    topic_docs[topic].append(doc)

for topic, docs in topic_docs.items():
    if topic == -1:
        continue
        
    print(f"\n=== Topic {topic} ===")
    for d in docs[:5]:  # show first 5 examples
        print("-", d)

from collections import defaultdict

topic_docs = defaultdict(list)

for doc, topic in zip(cleaned_tasks, topics):
    topic_docs[topic].append(doc)

for topic, docs in topic_docs.items():
    if topic == -1:
        continue
        
    print(f"\n=== Topic {topic} ===")
    for d in docs[:5]:  # show first 5 examples
        print("-", d)

info = topic_model.get_topic_info()

for _, row in info.iterrows():
    topic = row["Topic"]
    if topic == -1:
        continue
        
    print(f"\n=== Topic {topic} ===")
    print("Keywords:", topic_model.get_topic(topic))
    
    examples = [cleaned_tasks[i] for i in range(len(topics)) if topics[i] == topic]
    
    print("Examples:")
    for ex in examples[:3]:
        print("-", ex)

topic_model.visualize_topics()

print()

print('embeddings')

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(cleaned_tasks)

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(embeddings)

from collections import defaultdict

clusters = defaultdict(list)

for text, label in zip(cleaned_tasks, labels):
    clusters[label].append(text)

for k, v in clusters.items():
    print(f"\nCluster {k}:")
    for t in v[:5]:
        print("-", t)

print()

print('vectorise')

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_tasks)

from sklearn.decomposition import LatentDirichletAllocation

lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

words = vectorizer.get_feature_names_out()

for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print([words[j] for j in topic.argsort()[-10:]])

topic_assignments = lda.transform(X)
labels = topic_assignments.argmax(axis=1)

print(labels)