# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:24:16 2020

@author: Kylian Rijnbergen
"""

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import csv

words = pd.read_table("D:/Bachelor_Thesis/glove.840B.300d/glove.6B.50d.txt", sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)

#function for getting the vector of a word.
def vec(w):
    try:
        return words.loc[w].as_matrix()
    except:
        pass


#function for getting the closest word.    
words_matrix = words.as_matrix()

def find_closest_word(v):
    diff = words_matrix - v
    delta = np.sum(diff * diff, axis = 1)
    i = np.argmin(delta)
    return words.iloc[i].name

#Definition of class "BagOfWords"
class BagOfWords:
    """
    BagOfWords converts a string to a bag of words. Attributes: matrix, tokens
    """
    
    def __init__(self, string):
        vectorizer = CountVectorizer()
        self.matrix = vectorizer.fit_transform(string.split(" "))
        self.tokens = vectorizer.get_feature_names()

#Definition of class "MailVector
class MailVector:
    """ 
    The class MailVector vectorizes Emails.
    """
    
    def __init__(self, mailstring):
        self.mailstring = mailstring
        self.matrix = BagOfWords(mailstring).matrix
        self.tokens = BagOfWords(mailstring).tokens
        self.all_vectors = pd.DataFrame(columns = np.arange(0, 51))
        self.vectorize()
        self.get_average_vector()
        
            
    def vectorize(self):
        for index in range(0, len(self.tokens)):
            word = self.tokens[index]
            wordvec = vec(word)
            for i in range(0, 50):
                if wordvec is not None: 
                    self.all_vectors.loc[index, 0] = word
                    self.all_vectors.loc[index, i + 1] = wordvec[i]

    def get_average_vector(self):
        df = self.all_vectors[np.arange(1,51)]
        self.avg_vector = df.mean()                       