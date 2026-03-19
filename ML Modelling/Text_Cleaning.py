import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import spacy
import Text_Cleaning as TC

nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))
task_words = ['prize', 'live', 'team']
lemmatizer = WordNetLemmatizer()

def clean_task_description(task_description_text):

    task_description = task_description_text.copy()

    task_description = task_description.str.lower()

    task_description = task_description.apply(nltk.word_tokenize)

    task_description = task_description.apply(lambda x: [w for w in x if w.isalpha()])

    task_description = task_description.apply(lambda x: [w for w in x if w not in stop_words and w not in task_words])

    task_description = task_description.apply(lambda x: [w for w in x if len(w) > 2])

    task_description = task_description.apply(lambda x: [lemmatizer.lemmatize(w) for w in x])

    task_description = task_description.apply(lambda x: " ".join(x))

    return(task_description)


