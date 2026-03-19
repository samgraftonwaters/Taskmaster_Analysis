import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import spacy

nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
task_words = ['prize', 'live', 'team']
lemmatizer = WordNetLemmatizer()


task_description = task_description.str.lower()

task_description = task_description.apply(nltk.word_tokenize)

task_description = task_description.apply(lambda x: [w for w in x if w.isalpha()])

task_description = task_description.apply(lambda x: [w for w in x if w not in stop_words and w not in task_words])

task_description = task_description.apply(lambda x: [w for w in x if len(w) > 2])

task_description = task_description.apply(lambda x: [lemmatizer.lemmatize(w) for w in x])

task_description = task_description.apply(lambda x: " ".join(x))


