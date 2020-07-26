# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:27:28 2020

@author: Kylian Rijnbergen
"""

import pandas as pd #Pandas library for DataFrames
import math

def CutDataFrame(DataFrame_Name, Startrow, Endrow):
	Sliced_DataFrame = DataFrame_Name[Startrow: Endrow]
	return Sliced_DataFrame

Directory_Phishing_Mails = "D:/Bachelor_Thesis/APWG Phishing Emails/APWG Phishing Emails/" 
Df_Large_File_Data = pd.DataFrame() #Empty dataframe where our data will be stored.
FILESIZE = 1000 #Amount of rows in a new file.

List_Mail_Files = [
        "phish_month_8_2018", 
        "phish_month_9_2018", 
        "phish_month_10_2018", 
        "phish_month_11_2018", 
        "phish_month_12_2018", 
        "phish_month_1_2019", 
        "phish_month_2_2019", 
        "phish_month_3_2019"
        ]
    
for filename in List_Mail_Files:
    with open(Directory_Phishing_Mails + filename + ".json") as file_to_load:
        Df_Raw_File_Data = pd.read_json(file_to_load)
        length = len(Df_Raw_File_Data)
        file_amount = math.ceil(length/FILESIZE)
        for index in range(0, file_amount):
            Sliced_DataFrame = CutDataFrame(Df_Raw_File_Data, index * FILESIZE, (index + 1) * FILESIZE)
            Sliced_DataFrame.to_csv("D:/Bachelor_Thesis/Sliced_Email_Files/" + filename + "_" + str((index + 1)) + ".csv")
    del Df_Raw_File_Data