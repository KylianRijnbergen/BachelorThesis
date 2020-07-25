# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:24:16 2020
@author: Kylian Rijnbergen
"""

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import csv

words = pd.read_table("C:/Users/Kylian Rijnbergen/Documents/TBK/Year_3/Module 12/glove.6B.300d.txt", sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)

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
        self.words_one_hot = vectorizer.fit_transform(string.split(" ")).toarray()
        self.tokens = vectorizer.get_feature_names()

#Definition of class "MailVector
class MailVector:
    """ 
    The class MailVector vectorizes Emails.
    """
    
    def __init__(self, mailstring):
        self.mailstring = str(mailstring)
        words_one_hot = BagOfWords(self.mailstring).words_one_hot
        self.word_counts = np.sum(words_one_hot, axis = 0)
        self.tokens = BagOfWords(self.mailstring).tokens
        self.all_vectors = pd.DataFrame(columns = np.arange(0, 301))
        self.vectorize()
        self.get_average_vector()
        self.get_weighted_average_vector()
        
            
    def vectorize(self):
        for index in range(0, len(self.tokens)):
            word = self.tokens[index]
            wordvec = vec(word)
            for i in range(0, 300):
                if wordvec is not None: 
                    self.all_vectors.loc[index, 0] = word
                    self.all_vectors.loc[index, i + 1] = wordvec[i]

    def get_average_vector(self):
        df = self.all_vectors[np.arange(1,301)]
        self.avg_vector = df.mean()    

    def get_weighted_average_vector(self):
        df = self.all_vectors[np.arange(0,301)]
        self.weighted_avg_vector = df
        sum_vector = np.zeros(300) 
        total = 0
        for word in self.tokens:
            index = self.tokens.index(word)
            count = self.word_counts[index]
            wordvec = vec(word)
            if wordvec is not None:
                sum_vector = sum_vector + wordvec * count
                total += 1 * count
        self.weighted_vector = sum_vector/total
            
            