import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
warnings.filterwarnings('ignore')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import string, nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
nltk.download('wordnet')
nltk.download('omw-1.4')

df = pd.read_csv('javascript/peocessing/fake reviews dataset.csv')
# Define a function to clean text
def clean_text(text):
    nopunc = [w for w in text if w not in string.punctuation]
    nopunc = ''.join(nopunc)
    return ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])

df['text_'] = df['text_'].astype(str).apply(clean_text)

# Apply the preprocess function to the 'text_' column
def preprocess(text):
    return ' '.join([word for word in word_tokenize(text) if word not in stopwords.words('english') and not word.isdigit()])

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

df.dropna(inplace=True)
df['length'] = df['text_'].apply(len)
df[df['label']=='OR'][['text_','length']].sort_values(by='length',ascending=False).head().iloc[0].text_
def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]



bow_transformer = CountVectorizer(analyzer=text_process)
bow_transformer
bow_transformer.fit(df['text_'])
print("Total Vocabulary:",len(bow_transformer.vocabulary_))

review4 = df['text_'][3]
review4


bow_msg4 = bow_transformer.transform([review4])
bow_reviews = bow_transformer.transform(df['text_'])
tfidf_transformer = TfidfTransformer().fit(bow_reviews)
tfidf_rev4 = tfidf_transformer.transform(bow_msg4)
print(bow_msg4)
tfidf_reviews = tfidf_transformer.transform(bow_reviews)

review_train, review_test, label_train, label_test = train_test_split(df['text_'],df['label'],test_size=0.35)
pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',LogisticRegression())
])
pipeline.fit(review_train,label_train)

import pandas as pd

p1 = pd.read_csv('data.csv')
p2 = pd.read_csv('analysis.csv')

for index, row in p1.iterrows():
    if pipeline.predict([row['feedback']])[0] == "OR":
        p2 = pd.concat([pd.DataFrame(row).transpose(), p2], ignore_index=True)


p2.to_csv('analysis.csv', index=False)
