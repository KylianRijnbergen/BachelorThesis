# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:27:28 2020

@author: Kylian Rijnbergen
"""

import pandas as pd #Pandas library for DataFrames
from datetime import datetime #Get current date and time, this is later used to create new files automatically.
import Functions as Fn #Import Functions from Functions.py 
import DataFrameFunctions as DfFun #Import DataFrameFunctions
import ErikMichelle as EM 
import os


#Declaring debugging / setting variables
#Directory_Phishing_Mails = "D:/Bachelor_Thesis/Sliced_Email_Files/" #Directory where CSV files are stored.
Df_Raw_Data = pd.DataFrame() #Empty dataframe where our data will be stored.
#List_Mail_Files = [
#        "phish_month_1_2019_1"
#        ]

Directory_Sliced_Emails = "D:/Bachelor_Thesis/Sliced_Email_Files/"
os.chdir(Directory_Sliced_Emails)
List_Mail_Files = os.listdir()

    
#Load files and add contents to Pandas Dataframe "Df_Raw_Data".
#for Filename in List_Mail_Files:
Filename = List_Mail_Files[0]
with open(Directory_Sliced_Emails + Filename, encoding = "utf-8") as File_To_Load:
    Df_Raw_Data = pd.read_csv(File_To_Load)
        


#List of all headers for our data.
List_Data_Headers = [
        "id", 
        "date_sent", 
        "date_received", 
        "date_reported", 
        "links", 
        "sender_email", 
        "recipient_email", 
        "email_subject", 
        "email_raw_headers", 
        "email_raw_body", 
        "email_has_attachments", 
        "modified"
        ]

#List for all headers where the data has the format "timestamp". Datatype is np.int64
List_Data_Dates = [
        "date_sent", 
        "date_received", 
        "date_reported"
        ]

#List of all columns that need to be added.
List_Columns_For_Features = [
        "IsPhishing", 
        "Error",
        "Seen_Before",
        "Sender_Email_Address",
        "URLs_in_email"
        ]

#This is where we modify the DataFrame and preprocess our data for labelling.
#Loop over all rows
for Index in range(0, len(Df_Raw_Data)):

    #Set feature columns with blank value.
    for feature in List_Columns_For_Features:
        DfFun.WriteToDataFrame("", Index, feature, Df_Raw_Data)

    #Loop over all Columns
    for Header in List_Data_Headers:
    
        #Get data of a single sample.
        Data = DfFun.GetFromDataFrame(Index, Header, Df_Raw_Data)

        #If the value is a date, convert to dd/mm/yyyy format.
        if Header in List_Data_Dates: #Checks if Data is in format Timestamp by comparing Headers.
            if Data > 0: #Timestamp has to be positive. This is not the case in the raw data, this needs to be addressed.
                Data = pd.datetime.fromtimestamp(Data) #Convert Timestamp to DateTime format using Pandas.
                DfFun.WriteToDataFrame(Data, Index, Header, Df_Raw_Data) #Write Data to the DataFrame.
        
        #If the value is a sender email, retrieve the email and username. In case these are not found, leave them blank.
        elif Header == "sender_email": #Checks if entry may contain email address.
            Email_Address = Fn.Retreive_Email_Addresses(Data)
            if len(Email_Address) == 0:
                Email_Address = [""]
            
            #Write Email Address to Sender_Email_Address    
            DfFun.WriteToDataFrame(Email_Address[-1], Index, "Sender_Email_Address", Df_Raw_Data)

            #Write Username to the field Sender_Email_Username
            Email_Username = Fn.Get_Email_Username(Data, Fn.ListToString(Email_Address[-1]))
                           
            if len(Email_Username) != 0:
                Email_Username = Fn.ListToString(Email_Username, " ")
                DfFun.WriteToDataFrame(Email_Username, Index, "Sender_Email_Username", Df_Raw_Data)
            else:
                DfFun.WriteToDataFrame("", Index, "Sender_Email_Username", Df_Raw_Data)






Df_Filtered_Data_Full = EM.create_columns(Df_Raw_Data)

for Index in range(0, len(Df_Filtered_Data_Full)):
    Data = DfFun.GetFromDataFrame(Index, "body_readable", Df_Filtered_Data_Full)
    URL_List = Fn.Retreive_URLs(Data)
    URL_String = Fn.ListToString(URL_List, " ")
    DfFun.WriteToDataFrame(URL_String, Index, "URLs_in_Email", Df_Filtered_Data_Full)

    

#This is where we start labelling the Emails.
#Printing Emails
Get_Next = True
Items_Left = DfFun.Get_DataFrame_RowCount(Df_Filtered_Data_Full)
while Get_Next and Items_Left != 0:
    CurrentRow = Fn.Get_Data_Not_Seen(Df_Filtered_Data_Full)
    for i in range(0, 5):
        print("")
    Fn.Print_Email(CurrentRow, Df_Filtered_Data_Full)
    print("Is this a Phishing Email? [True (1)/False(0)/Skip(s)/Exit(e)]: ")
    Phishing_Value = input()
    if Phishing_Value == "e":
        Get_Next = bool(False)
    elif Phishing_Value == "0" or Phishing_Value == "1": 
        Df_Filtered_Data_Full.loc[CurrentRow, "IsPhishing"] = Phishing_Value
    else: 
        Df_Filtered_Data_Full.loc[CurrentRow, "Error"] = Phishing_Value
    Df_Filtered_Data_Full.loc[CurrentRow, "Seen_Before"] = "1"
    Items_Left -= 1

#Dropping columns
    #Note that email_raw_object MUST be dropped in order to write to CSV. This is due to the entry being of type (email.message.Message)
Columns_To_Drop = [  "email_raw_object"
        ]
 #This is a list of all columns
""" 
Columns_To_Drop = ["id",
"links",
"date_sent",
 "date_received",
 "date_reported",
 "email_subject",
 "modified",
 "IsPhishing",
 "Error",
 "Seen_Before",
 "Sender_Email_Address",
 "Sender_Email_Username",
 "date",
 "return-path",
 "local_time",
 "body_words",
"sender_email", 
"recipient_email",
"email_raw_headers",
"email_raw_body",
"email_has_attachments",
"email_raw_total",
"email_raw_object",
"from",
"to",
"subject",
"content-type",
"body_raw",
"body_text",
"addresses"]
"""

Df_Filtered_Data_Dropped = Df_Filtered_Data_Full.drop(columns = Columns_To_Drop)

#Write to CSV 
#print("Write to CSV? [True/False]: ")
#Comment in line below gives option not to write to CSV. As Datetime is now included, though, this defaults to True.
To_Csv = True #bool(input())
if To_Csv:
    Current_Date_And_Time = datetime.now()
    Current_Date_And_Time_String = Current_Date_And_Time.strftime("%d_%m_%Y_%H_%M_%S")
    Df_Filtered_Data_Dropped.to_csv("D:/Bachelor_Thesis/Labelled_Email_Files/_" + Filename + "_" + Current_Date_And_Time_String + "Parts_Labelled.csv")