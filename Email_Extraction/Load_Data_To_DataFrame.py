# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:27:28 2020

@author: Kylian Rijnbergen
"""

import pandas as pd #Pandas library for DataFrames
from datetime import datetime #Get current date and time, this is later used to create new files automatically.
import Functions as Fn #Import Functions from Functions.py 

#Declaring debugging / setting variables
#Directory_Phishing_Mails = "D:/Bachelor_Thesis/APWG Phishing Emails/APWG Phishing Emails/" #Directory where JSON files are stored.
Directory_Phishing_Mails = "D:/Bachelor_Thesis/Email_Extraction/"
Reload = True
Load_All = False
Headers_All = True


#Reloading of dataframe.
if Reload: 
    Df_Raw_Data = pd.DataFrame() #Empty dataframe where our data will be stored.
    #Mail files contained in Directory_Phishing_Mails. If Load_All is set to True, all files are loaded. If False, only "phish_month_8_2018" is loaded. This is the smallest file.
    if Load_All:
        List_Mail_Files = ["phish_month_8_2018", "phish_month_9_2018", "phish_month_10_2018", "phish_month_11_2018", "phish_month_12_2018", "phish_month_1_2019", "phish_month_2_2019", "phish_month_3_2019"]
    else:
        List_Mail_Files = ["Debugging_File_100_Rows_Only"]	
    #Load files and add contents to Pandas Dataframe "Df_Raw_Data".
    for Filename in List_Mail_Files:
        with open(Directory_Phishing_Mails + Filename + ".json") as File_To_Load:
            Df_Raw_File_Data = pd.read_json(File_To_Load)
            Df_Raw_Data = Df_Raw_Data.append(Df_Raw_File_Data)
        del Df_Raw_File_Data

#Lines below create a debugging file.
#Debugging_File = Fn.CutDataFrame(Df_Raw_Data, 0, 100)
#Debugging_File.to_json("D:/Bachelor_Thesis/Email_Extraction/Debugging_File_100_Rows_Only.json")

#If Headers_All is set to true, all headers are loaded. If False, only alternative is loaded.
if Headers_All:
    List_Data_Headers = ["id", "date_sent", "date_received", "date_reported", "links", "sender_email", "recipient_email", "email_subject", "email_raw_headers", "email_raw_body", "email_has_attachments", "modified"] #List of all headers
else:
    List_Data_Headers = ["sender_email"]
List_Data_Dates = ["date_sent", "date_received", "date_reported"] #List for all headers where the data has the format "timestamp". Datatype is np.int64


for Header in List_Data_Headers: #Loop over all Columns
    for Index in range(0, len(Df_Raw_Data)): #Loop over all Rows.
        Df_Raw_Data.loc[Index, "IsPhishing"] = "" #Fill with null values
        Df_Raw_Data.loc[Index, "Error"] = "" #Debugging purposes only. Set error.
        Df_Raw_Data.loc[Index, "Seen_Before"] = "0"
        Data = Df_Raw_Data.loc[Index,Header] #Retreive value and assign it to "Data".
        if Header in List_Data_Dates: #Checks if Data is in format Timestamp by comparing Headers.
            if Data > 0: #Timestamp has to be positive. This is not the case in the raw data, this needs to be addressed.
                Data = pd.datetime.fromtimestamp(Data) #Convert Timestamp to DateTime format using Pandas.
                Df_Raw_Data.loc[Index, Header] = Data #Assigns DateTime format to Cell in Df_Raw_Data.
        
        elif Header == "sender_email": #Checks if entry may contain email address.
            Email_Address = Fn.Retreive_Email_Addresses(Data)
            if len(Email_Address) == 0:
                Email_Address = [""]
                
            Df_Raw_Data.loc[Index, "Sender_Email_Filtered"] = Email_Address[-1]
            Email_Username = Fn.Get_Email_Username(Data, Fn.ListToString(Email_Address[-1]))
                           
            if len(Email_Username) != 0:
                Df_Raw_Data.loc[Index, "Sender_Email_Username"] = Fn.ListToString(Email_Username, " ")
            else:
                Df_Raw_Data.loc[Index, "Sender_Email_Username"] = ""


#Printing Emails
Get_Next = True
Items_Left = Fn.Get_DataFrame_RowCount(Df_Raw_Data)
while Get_Next and Items_Left != 0:
    CurrentRow = Fn.Get_Data_Not_Seen(Df_Raw_Data)
    Fn.Print_Email(CurrentRow, Df_Raw_Data)
    print("Is this a Phishing Email? [True (1)/False(0)/Skip(s)/Exit(e)]: ")
    Phishing_Value = input()
    if Phishing_Value == "e":
        Get_Next = bool(False)
    elif Phishing_Value == "0" or Phishing_Value == "1": 
        Df_Raw_Data.loc[CurrentRow, "IsPhishing"] = Phishing_Value
    else: 
        Df_Raw_Data.loc[CurrentRow, "Error"] = Phishing_Value
    Df_Raw_Data.loc[CurrentRow, "Seen_Before"] = "1"
    Items_Left -= 1

#Dropping columns
Columns_To_Drop = ["links", "sender_email"]          
Df_Filtered_Data = Df_Raw_Data.drop(columns = Columns_To_Drop)

#Write to CSV 
print("Write to CSV? [True/False]: ")
#Comment in line below gives option not to write to CSV. As Datetime is now included, though, this defaults to True.
To_Csv = True #bool(input())
if To_Csv:
    Current_Date_And_Time = datetime.now()
    Current_Date_And_Time_String = Current_Date_And_Time.strftime("%d_%m_%Y_%H_%M_%S")
    Df_Filtered_Data.to_csv("D:/Bachelor_Thesis/Email_Extraction/Raw_Data_Csv_File_" + Filename + "_" + Current_Date_And_Time_String + ".csv")