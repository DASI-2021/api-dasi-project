# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 01:04:33 2021

@author: JHOHAN
"""

# information-extraction.py

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

string = """
Hey,
This week has been crazy. Attached is my report on IBM. Can you give it a quick read and provide some feedback.
Also, make sure you reach out to Claire (claire@xyz.com).
You're the best.
Cheers,
George W.
212-555-1234

Some economists have responded positively to Bitcoin, including 
Francois R. Velde, senior economist of the Federal Reserve in Chicago 
who described it as "an elegant solution to the problem of creating a 
digital currency." In November 2013 Richard Branson announced that 
Virgin Galactic would accept Bitcoin as payment, saying that he had invested 
in Bitcoin and found it "fascinating how a whole new global currency 
has been created", encouraging others to also invest in Bitcoin.
Other economists commenting on Bitcoin have been critical. 
Economist Paul Krugman has suggested that the structure of the currency 
incentivizes hoarding and that its value derives from the expectation that 
others will accept it as payment. Economist Larry Summers has expressed 
a "wait and see" attitude when it comes to Bitcoin. Nick Colas, a market 
strategist for ConvergEx Group, has remarked on the effect of increasing 
use of Bitcoin and its restricted supply, noting,jho@gmail.com "When incremental 
adoption meets relatively fixed supply, it should be no surprise that 
prices go up. And that’s exactly what is happening to BTC prices.
"""

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

if __name__ == '__main__':
    numbers = extract_phone_numbers(string)
    emails = extract_email_addresses(string)
    names = extract_names(string)