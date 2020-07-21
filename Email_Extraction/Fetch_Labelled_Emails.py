import pandas as pd #Pandas library for DataFrames
from datetime import datetime
import os

#Declaring debugging / setting variables
Directory_Labelled_Emails = "D:/Bachelor_Thesis/Labelled_Email_Files/"
os.chdir(Directory_Labelled_Emails)
List_Mail_Files = os.listdir()

#Create DataFrame Df_Data, which will contain all data in the labelled mails file.
Df_Data = pd.DataFrame()
for filename in List_Mail_Files:
    with open(Directory_Labelled_Emails + filename, encoding = "utf-8") as File_To_Load:
        Df_Raw_File_Data = pd.read_csv(File_To_Load)
        A = Df_Raw_File_Data.loc[Df_Raw_File_Data["IsPhishing"] == 0]
        B = Df_Raw_File_Data.loc[Df_Raw_File_Data["IsPhishing"] == 1]
        Df_Data = Df_Data.append(A)
        Df_Data = Df_Data.append(B)    
    del Df_Raw_File_Data

#Write to CSV
Current_Date_And_Time = datetime.now()
Current_Date_And_Time_String = Current_Date_And_Time.strftime("%d_%m_%Y_%H_%M_%S")
Df_Data.to_csv("D:/Bachelor_Thesis/Labelled_Emails_Only/" + filename + "_" + Current_Date_And_Time_String + ".csv")
#write to XLSX
Df_Data.to_excel("D:/Bachelor_Thesis/Labelled_Emails_Only/" + filename + "_" + Current_Date_And_Time_String + ".xlsx")