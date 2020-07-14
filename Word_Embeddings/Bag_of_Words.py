# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 10:26:33 2020

@author: Kylian Rijnbergen
"""

from sklearn.feature_extraction.text import CountVectorizer

class TextToBow:
    
    def __init__(self, mail_string):
        
        self.string = mail_string
        vectorizer = CountVectorizer()
        self.matrix = vectorizer.fit_transform(StringToList(mail_string))
        self.tokens = vectorizer.get_feature_names()