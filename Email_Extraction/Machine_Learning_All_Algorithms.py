# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:33:35 2020

@author: Kylian Rijnbergen
"""

#Self-Written Functions
import DataFrameFunctions as DfFun

#Data-Handling Libraries
import pandas as pd 
import numpy as np 

#Sklearn Libraries-General
from sklearn.model_selection import train_test_split 
#Sklearn Libraries-Specific
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from class_performance_metrics import PerformanceMetrics
import pickle

 
#Selecting which files to load.
Directory_Labelled_Emails = "D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/"
List_Mail_Files =  ["nan_removed"]	

Df_Data = pd.DataFrame()
load_Augmented = True #True loads augmented, false loads normal.

if load_Augmented == True:
    #Load files and add contents to Pandas Dataframe "Df_Raw_Data".
    for Filename in List_Mail_Files:
        with open(Directory_Labelled_Emails + Filename + ".csv") as File_To_Load:
            Df_Raw_File_Data = pd.read_csv(File_To_Load)
            Df_Data = Df_Data.append(Df_Raw_File_Data)
        del Df_Raw_File_Data
    
    
      
    del Directory_Labelled_Emails
    del Filename
    del List_Mail_Files
else:
    Df_Data = pd.read_excel("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/300_Dimensions.xlsx", index_col = None)

Np_Data = Df_Data.to_numpy()


Np_Feature_Vectors = np.delete(Np_Data, [0, 1, 2], axis = 1)

Labels = DfFun.GetColumnFromDataFrame(Df_Data, "Label")
Np_Labels = Labels.to_numpy()



##### TRAINING PART

Start = 0
End = 5


classifiers = [
        #svm.SVC(kernel = "rbf", gamma = "scale"),
        #RandomForestClassifier(n_estimators = 1000, max_depth = 2),
        MLPClassifier(solver = "lbfgs", alpha = 0.0005, hidden_layer_sizes = (5000,200)),
        #LogisticRegression(solver = "lbfgs"),
        #AdaBoostClassifier(n_estimators=5, learning_rate=1)
        ]

TEST_SIZE = 0.2
SCORE_ATTRIBUTES = [
        "classifier",
        "random_state",
        "test_size",
        "accuracy",
        "precision",
        "recall",
        "f1_score"
        ]
df_scores = pd.DataFrame(columns = SCORE_ATTRIBUTES)
for index in range(Start, End):
    print(index)
    X_train, X_test, y_train, y_test = train_test_split(Np_Feature_Vectors, Np_Labels, test_size = TEST_SIZE, random_state = index)
    for clf in classifiers:
        clf_position = classifiers.index(clf)
        clf.fit(X_train, y_train.ravel())
        y_pred = clf.predict(X_test)
        scores_for_run = PerformanceMetrics(clf, index, y_test, y_pred, TEST_SIZE)
        for attribute, value in scores_for_run.__dict__.items():
            df_scores.loc[index + (End-Start) * clf_position, attribute] = value
            
df_scores = df_scores.sort_index()
        
best_score = df_scores["accuracy"].max()    

print(best_score)

