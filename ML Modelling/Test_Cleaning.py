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

stop_words = set(stopwords.words('english'))




file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
task_data = pd.read_csv(file_path + 'Task Descriptions Cleaned.csv')

task_description = task_data['Description'].copy()

print(task_data.head())

import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
task_words = ['prize', 'live', 'team']
lemmatizer = WordNetLemmatizer()

# 1. Lowercase
task_description = task_description.str.lower()

# 2. Tokenize
task_description = task_description.apply(nltk.word_tokenize)

# 3. Remove punctuation x and non-alphabetic tokens
task_description = task_description.apply(lambda x: [w for w in x if w.isalpha()])

# 4. Remove stopwords and custom task words
task_description = task_description.apply(lambda x: [w for w in x if w not in stop_words and w not in task_words])

# 5. Remove short words (<=2 chars)
task_description = task_description.apply(lambda x: [w for w in x if len(w) > 2])

# 6. Lemmatization
task_description = task_description.apply(lambda x: [lemmatizer.lemmatize(w) for w in x])
print(task_description.head())
# 7. Optional: convert back to string
task_description = task_description.apply(lambda x: " ".join(x))

print(task_description.head())

task_description = task_description.str.lower()

task_description = task_description.apply(nltk.word_tokenize)

task_description = task_description.apply(
    lambda x: [c + " " if c in string.punctuation else c for c in x])

task_description = task_description.str.replace(r"[{}]".format(re.escape(string.punctuation)), '', regex = True)

task_words = ['prize', 'live', 'team']

task_description = task_description.apply(lambda x: [w for w in x if w not in stop_words and w not in task_words])

task_description = task_description.apply(
    lambda x: [w for w in x if w.isalpha()])

print(task_description.head())


task_description = task_description.apply(lambda x: [w for w in x if len(w) > 2])

print(task_description.head())

lemmatizer = WordNetLemmatizer()

task_description = task_description.apply(
    lambda x: [lemmatizer.lemmatize(w) for w in x]
)

print(task_description.head())

task_description = task_description.str.replace(r'\s+', ' ', regex=True)

print(task_description.head())


# .apply(
#     lambda x: " ".join(
#         w for w in nltk.word_tokenize(x.lower())
#         if w not in stop_words and w not in string.punctuation
#     )
# )