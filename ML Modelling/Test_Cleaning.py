import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')

import spacy
nlp = spacy.load("en_core_web_sm")

import string
import re


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

print(task_data.head())

def remove_punct(ptext):
    # replace any punctuation with nothing "", effectively removing it
    ptext = re.sub(string=ptext,
                   pattern="[{}]".format(string.punctuation), 
                   repl="")
    return ptext

def clean_stopwords(tokens):
    # define stopwords
    stop_words = set(stopwords.words('english'))
    # loop through each token and if the word isn't in the set 
    # of stopwords keep it
    return [item for item in tokens if item not in stop_words]

task_data['Description'] = task_data['Description'].str.lower()

print(task_data.head())

task_data['Description'] = task_data['Description'].str.replace(
        r'([{}])'.format(re.escape(string.punctuation)),
        r'\1 ',
        regex=True)

task_data['Description'] = task_data['Description'].str.replace(
    r'([{}])'.format(re.escape(string.punctuation)), r'\1 ', regex=True
).str.replace(r'\s+', ' ', regex=True)

task_data['Description'] = task_data['Description'].apply(
    lambda x: " ".join([c + " " if c in string.punctuation else c for c in x]).split())
print(task_data.head())

task_data['Description'] = task_data['Description'].str.replace(r'\s+', ' ', regex=True)
print(task_data.head())

task_data['Description'] = task_data['Description'].apply(remove_punct)

print(task_data.head())

task_data['Description'] = task_data['Description'].apply(clean_stopwords)

print(task_data.head())