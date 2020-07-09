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
from sklearn import metrics
#Sklearn Libraries-Specific
from sklearn import svm


#Selecting which files to load.
Directory_Labelled_Emails = "D:/Bachelor_Thesis/Email_Extraction/"
List_Mail_Files =  ["Raw_Data_Csv_File_Raw_Data_Csv_File_Debugging_File_100_Rows_Only_05_07_2020_15_12_07_05_07_2020_15_14_23"]	


#Load al files to DataFrame
Df_Data = pd.DataFrame()
for Filename in List_Mail_Files:
    with open(Directory_Labelled_Emails + Filename + ".csv") as File_To_Load:
        Df_Raw_File_Data = pd.read_csv(File_To_Load)
        Df_Data = Df_Data.append(Df_Raw_File_Data)


#Convert to NumPy
Np_Data = Df_Data.to_numpy()
Np_Feature_Vectors = np.delete(Np_Data, [0, 1, 4], axis = 1) #Delete unnecessary columns.

#Create Label Array
Labels = DfFun.GetColumnFromDataFrame(Df_Data, "Label")
Np_Labels = Labels.to_numpy()




Start = 0
End = 1


for index in range(Start, End):
    print(index)
    X_train, X_test, y_train, y_test = train_test_split(Np_Feature_Vectors, Np_Labels, test_size = 0.2, random_state = index)
    clf = svm.SVC(kernel = "rbf", gamma = "scale")
    clf.fit(X_train, y_train.ravel())
    y_pred = clf.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    print("Precision:",metrics.precision_score(y_test, y_pred))
    print("Recall:",metrics.recall_score(y_test, y_pred))
    del clf
    


