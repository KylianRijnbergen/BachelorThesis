# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:24:16 2020

@author: Kylian Rijnbergen
"""

from Bag_of_Words import TextToBow
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

#Definition of class "MailVector
class MailVector:
    """ 
    The class MailVector stores mail ID, and a vector containing a matrix of all of it's word vectors.
    """
    
    def __init__(self, mailstring):
        self.mailstring = mailstring
        self.all_vectors = pd.DataFrame(columns = np.arange(0, 51))
        self.vectorize()
        self.get_average_vector()
        
        
    def get_bag_of_words(self):
        return TextToBow(self.mailstring)
            
    def vectorize(self):
        for index in range(0, len(self.get_bag_of_words().tokens)):
            word = self.get_bag_of_words().tokens[index]
            wordvec = vec(word)
            for i in range(0, 50):
                if wordvec is not None: 
                    self.all_vectors.loc[index, 0] = word
                    self.all_vectors.loc[index, i + 1] = wordvec[i]

    def get_average_vector(self):
        df = self.all_vectors[np.arange(1,51)]
        self.avg_vector = df.mean()
        
                    
                       