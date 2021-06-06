import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import re
import nltk
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.corpus import stopwords

import json

stop = stopwords.words('english')

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


class ExtractionAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # print("ExtractionAgent: Agent running")

            msg = await self.receive(timeout=1)
            result = ""

            if msg:
                print("ExtractionAgent: Message received with content: {}".format(msg.body))

                result += "Phones: " + str(extract_phone_numbers(msg.body))
                result += "Emails: " + str(extract_email_addresses(msg.body))
                result += "Names: " + str(extract_names(msg.body))

                myDict = {'phones':extract_phone_numbers(msg.body), 'emails':extract_email_addresses(msg.body), 'names':extract_names(msg.body)}
                jsonStr = json.dumps(myDict)

                msg = Message(to=self.agent.recv_jid)  # Instantiate the message
                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                # msg.body = str(f"ExtractionAgent: Message Received {datetime.datetime.now().time()}, Result: {result}")
                msg.body = str(f"{jsonStr}")
                await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ExtractionAgent: started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
    
    def __init__(self, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        super().__init__(*args, **kwargs)
