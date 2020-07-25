# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:11:47 2020

@author: Kylian Rijnbergen
"""
from sklearn import metrics

class PerformanceMetrics:
    
    """ This class stores performance metrics for a certain algorithm. """
    
    def __init__(self, classifier, random_state, y_test, y_pred, *test_size):
        self.classifier = classifier
        self.random_state = random_state
        self.test_size = test_size
        self.get_accuracy(y_test, y_pred)
        self.get_precision(y_test, y_pred)
        self.get_recall(y_test, y_pred)
        self.get_f1_score(y_test, y_pred)
        #self.get_roc_curve(y_test, y_pred)
        
    def get_accuracy(self, y_test, y_pred):
        self.accuracy = metrics.accuracy_score(y_test, y_pred)
    
    def get_precision(self, y_test, y_pred):
        self.precision = metrics.precision_score(y_test, y_pred)
        
    def get_recall(self, y_test, y_pred):
        self.recall = metrics.recall_score(y_test, y_pred)
    
    def get_f1_score(self, y_test, y_pred):
        self.f1_score = metrics.f1_score(y_test, y_pred)
    
    def get_roc_curve(self, y_test, y_pred):
        self.roc_curve = metrics.roc_curve(y_test, y_pred)
        
        