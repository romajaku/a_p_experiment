
import pickle
import os
import subprocess
import sys
try:
    import pandas as pd
except:
    print("pandas not found! installing....")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

try:
    import nltk
except:
    print("nltk not found! installing....")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])

from nltk.tokenize import word_tokenize
from nltk.corpus.reader import nkjp
from nltk.tokenize import word_tokenize

try:
    import spacy
except:
    print("spacy not found! installing....")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])



def estimateFreq(stimuliDf):
    """
        Estimates sentence Frequency based solely on frequency of Lemmas in a given sentence.

        First it filters out stopwords, then lemmatize the system, and at last compares the tokens to
        the frequency of lemmas estimated with NKJP corpus

        Arguments: 
            stimuliDf - a Df which has a column named "Sentences" containing Sentences at hand
        Returns: 
            sentenceFreq - Detailed look into frequency of each word in every Sentence
            summaryFreq  - a Freq of a whole sentence
            tokenizedSen - a list of tokenized sentences as a double check
    """

    # Open Frequency Dictiionary 
    with open('PLFreqDict.pickle', 'rb') as handle:
        UniqueWordsDictionary = pickle.load(handle)

    # Load Spacy Lemmatizer 
    nlp = spacy.load("pl_core_news_sm", disable = ['parser','ner'])

    # Open Polish Stopwords
    global plstopwords
    f = open("polish.stopwords.txt", "r", encoding='utf-8')
    plstopwords = f.read().split("\n")

    # Gather data from sentences  Sentence Data
    sentences = list(stimuliDf['Sentences'])

    tokenizedSen = []
    sentenceFreq = []
    avgFreq = []
    for sen in sentences:
        sentenceFreqTemp = []
        sen = sen.replace('.','') #removing dots 
        doc = nlp(sen.lower())

        tokenSentence = [i.lemma_ for i in doc if i.lemma_ not in plstopwords]
        for i in tokenSentence:
            if i in list(UniqueWordsDictionary.keys()):
                sentenceFreqTemp.append(UniqueWordsDictionary[i])
            else:
                sentenceFreqTemp.append(0)
        
        sentenceFreq.append(sentenceFreqTemp)
        avgFreq.append(int(sum(sentenceFreqTemp)/len(sentenceFreqTemp)))
        tokenizedSen.append(tokenSentence)

    return sentenceFreq,avgFreq,tokenizedSen


# creating a data frame
df = pd.read_csv("zdania.csv")
print(df.head())
[sentenceFreq, avgFreq, tokenizedSen] = estimateFreq(df)
df['sentenceFreq'] = pd.Series(sentenceFreq)
df['avgFreq'] = pd.Series(avgFreq)
df['tokenizedSen'] = pd.Series(tokenizedSen)

print(df)
df.to_csv('freqs.csv', encoding='utf-16')
