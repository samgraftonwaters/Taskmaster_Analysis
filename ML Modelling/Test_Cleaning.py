import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import spacy

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))




file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())


def clean_stopwords(tokens):
    # define stopwords
    
    # loop through each token and if the word isn't in the set 
    # of stopwords keep it
    return [item for item in tokens if item not in stop_words]

task_description = task_description.str.lower()

task_description = task_description.apply(
    lambda x: "".join([c + " " if c in string.punctuation else c for c in x])
)

task_description = task_description.str.replace(r'\s+', ' ', regex=True)


task_description = task_description.str.replace(r"[{}]".format(re.escape(string.punctuation)), '', regex = True)

task_words = ['prize', 'live', 'team']
task_description = task_description.apply(
    lambda x: " ".join([w for w in x.split() if w.lower() not in stop_words])).apply(
    lambda x: " ".join([w for w in x.split() if w.lower() not in task_words]))


print(task_description.head())
