# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:11:47 2020

@author: Kylian Rijnbergen
"""
from sklearn import metrics

def evaluate(y_test, y_pred):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    return accuracy, precision, recall, f1_score