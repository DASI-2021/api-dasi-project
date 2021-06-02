import datetime
import re

import joblib
# import nltk
import numpy as np
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


def get_classification(news):

    filename = 'finalized_model.sav'
    filename_vocabulary = 'finalized_vocabulary.sav'
    # load the model from disk
    loaded_model = joblib.load(filename)
    loaded_vocabulary = joblib.load(filename_vocabulary)
    classification_options = ['athletics', 'cricket', 'football', 'rugby', 'tennis']

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


class ClassificationAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # print("ClassificationAgent: Agent running")

            msg = await self.receive(timeout=1)
            
            if msg:
                print("ClassificationAgent: Message received with content: {}".format(msg.body))

                result = get_classification(msg.body)

                msg = Message(to=self.agent.recv_jid)  # Instantiate the message
                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"ClassificationAgent: Message Received {datetime.datetime.now().time()} , Result: {result}")
                await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ClassificationAgent: started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
    
    def __init__(self, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        super().__init__(*args, **kwargs)
