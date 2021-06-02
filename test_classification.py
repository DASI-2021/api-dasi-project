import re

import joblib
# import nltk
import numpy as np
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.datasets import load_files
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split

movie_data = load_files(r"dataset")
print(movie_data)
print(movie_data.target_names)
print(movie_data.target)
X, y = movie_data.data, movie_data.target

classification_options = ['athletics', 'cricket', 'football', 'rugby', 'tennis']

documents = []


stemmer = WordNetLemmatizer()

for sen in range(0, len(X)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(X[sen]))
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    
    documents.append(document)

# vectorizer = CountVectorizer(max_features=99, stop_words=stopwords.words('english'))
vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()

# tfidfconverter = TfidfTransformer()
# X = tfidfconverter.fit_transform(X).toarray()

print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(X_train, y_train) 

y_pred = classifier.predict(X_test)


print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))

filename = 'finalized_model.sav'
filename_vocabulary = 'finalized_vocabulary.sav'
joblib.dump(classifier, filename)
joblib.dump(vectorizer, filename_vocabulary)
 
# some time later...
 
# load the model from disk
loaded_model = joblib.load(filename)
loaded_vocabulary = joblib.load(filename_vocabulary)
y_pred = loaded_model.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))


string = """
Streak return could lift Zimbabwe
Capriati to miss Melbourne

Jennifer Capriati has become the third leading lady to withdraw from the Australian Open because of injury.

The organisers of the first grand slam of 2005, which begins on 17 January, said the American has a problem with her right shoulder. It comes as a blow to the women's draw as last year's champion, Justin Henin-Hardenne, and runner-up, Kim Clijsters, will also be absent. Capriati is a two-time champion in Melbourne with wins in 2001 and 2002. She is believed to have picked up the injury at the Advanta Championships at Philadelphia in November and had to pull out of an exhibition match with Wimbledon champion Maria Sharapova on 17 December. Capriati also decided against competing in the Australian Open warm-up event, the Sydney International. """



def get_classification(news):

    filename = 'finalized_model.sav'
    filename_vocabulary = 'finalized_vocabulary.sav'
    # load the model from disk
    loaded_model = joblib.load(filename)
    loaded_vocabulary = joblib.load(filename_vocabulary)

    documents = []
    stemmer = WordNetLemmatizer()

    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(news))
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    
    documents.append(document)

    print(documents)

    # vectorizer = CountVectorizer(max_features=99, stop_words=stopwords.words('english'))
    X = loaded_vocabulary.transform(documents).toarray()

    # tfidfconverter = TfidfTransformer()
    # X = tfidfconverter.fit_transform(X).toarray()

    y_pred = loaded_model.predict(X)
    print(y_pred)

    option = int(y_pred[0])

    return classification_options[option]


result = get_classification(string)
print(result)