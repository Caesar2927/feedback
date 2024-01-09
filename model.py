import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import string, nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the dataset
df = pd.read_csv('javascript/peocessing/fake reviews dataset.csv')

# Define a function to clean text
def clean_text(text):
    nopunc = [w for w in text if w not in string.punctuation]
    nopunc = ''.join(nopunc)
    return ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])

# Apply the clean_text function to the 'text_' column
df['text_'] = df['text_'].astype(str).apply(clean_text)

# Define a function for further preprocessing
def preprocess(text):
    return ' '.join([word for word in word_tokenize(text) if word not in stopwords.words('english') and not word.isdigit()])

# Apply the preprocess function to the 'text_' column
df['text_'] = df['text_'].apply(preprocess)

# Convert text to lowercase
df['text_'] = df['text_'].str.lower()

# Stemming
stemmer = PorterStemmer()
df['text_'] = df['text_'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))

# Lemmatization
lemmatizer = WordNetLemmatizer()
df['text_'] = df['text_'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Display the preprocessed text
print(df['text_'].head())

# Save the preprocessed dataset to a new CSV file
df.to_csv('Preprocessed_Fake_Reviews_Detection_Dataset.csv')
