# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 11:27:53 2020

@author: Kylian Rijnbergen
"""

import pandas as pd #Pandas library for DataFrames
import sklearn as sk
from sklearn.svm import SVC
from sklearn import svm
import matplotlib.pyplot as plt
import DataFrameFunctions as DfFun
import numpy as np
from datetime import datetime

#Declaring debugging / setting variables
Directory_Labelled_Emails = "D:/Bachelor_Thesis/Email_Extraction/"
List_Mail_Files =  ["Raw_Data_Csv_File_Debugging_File_100_Rows_Only_05_07_2020_15_12_07"]	

Df_Data = pd.DataFrame()
#Load files and add contents to Pandas Dataframe "Df_Raw_Data".
for Filename in List_Mail_Files:
    with open(Directory_Labelled_Emails + Filename + ".csv") as File_To_Load:
        Df_Raw_File_Data = pd.read_csv(File_To_Load)
        Df_Data = Df_Data.append(Df_Raw_File_Data)
    del Df_Raw_File_Data

Df_Numerical_Data = DfFun.GetColumnFromDataFrame(Df_Data, "id")
Attachments = DfFun.GetColumnFromDataFrame(Df_Data, "email_has_attachments")
Label = DfFun.GetColumnFromDataFrame(Df_Data, "IsPhishing")

Df_Numerical_Data["Attachments"] = Attachments

for index in range(0, len(Df_Numerical_Data)):
    Links = Df_Data.loc[index, "URLs_in_Email"]
    if type(Links) == str: 
        Df_Numerical_Data.loc[index, "length_of_links"] = len(Links)
    else: 
        Df_Numerical_Data.loc[index, "length_of_links"] = 0
        
Df_Numerical_Data["Label"] = Label
        

Df_Sorted = Df_Numerical_Data.sort_values(by = ["Label"])
A = Df_Sorted.loc[Df_Sorted["Label"] == 0]
B = Df_Sorted.loc[Df_Sorted["Label"] == 1]
Df_New = pd.DataFrame()
Df_New = Df_New.append(A)
Df_New = Df_New.append(B)

y = Df_New.iloc[:,3]
X = Df_New.iloc[:, :3]

To_Csv = True #bool(input())
if To_Csv:
    Current_Date_And_Time = datetime.now()
    Current_Date_And_Time_String = Current_Date_And_Time.strftime("%d_%m_%Y_%H_%M_%S")
    Df_New.to_csv("D:/Bachelor_Thesis/Email_Extraction/Raw_Data_Csv_File_" + Filename + "_" + Current_Date_And_Time_String + ".csv")

model = SVC(kernel ="linear")
model.fit(X, y)

def plot_svc_decision_function(model, ax=None, plot_support=True):
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # create grid to evaluate model
    x = np.linspace(xlim[0], xlim[1])
    y = np.linspace(ylim[0], ylim[1])
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)
    
    # plot decision boundary and margins
    ax.contour(X, Y, P, colors='k',
               alpha=0.5,
               linestyles=['--', '-', '--'])
    
    # plot support vectors
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0],
                   model.support_vectors_[:, 1],
                   s=300, linewidth=1, facecolors='none');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(model);


print(model.support_vectors_)
