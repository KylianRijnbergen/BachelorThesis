# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:27:28 2020

@author: Kylian Rijnbergen
"""

import pandas as pd #Pandas library for DataFrames
import re as regex #Import Regular Expressions
import Functions as Fn #Import Functions from Functions.py 



Directory_Phishing_Mails = "D:/Bachelor_Thesis/APWG Phishing Emails/APWG Phishing Emails/" #Directory where JSON files are stored.

#Mail files contained in Directory_Phishing_Mails. If Load_All is set to True, all files are loaded. If False, only "phish_month_8_2018" is loaded. This is the smallest file.
Load_All = False
if Load_All:
	List_Mail_Files = ["phish_month_8_2018", "phish_month_9_2018", "phish_month_10_2018", "phish_month_11_2018", "phish_month_12_2018", "phish_month_1_2019", "phish_month_2_2019", "phish_month_3_2019"]
else:
	List_Mail_Files = ["phish_month_12_2018"]


Df_Raw_Data = pd.DataFrame() #Empty dataframe where our data will be stored.

#Load files and add contents to Pandas Dataframe "Df_Raw_Data".
for Filename in List_Mail_Files:
	with open(Directory_Phishing_Mails + Filename + ".json") as File_To_Load:
		Df_Raw_File_Data = pd.read_json(File_To_Load)
		Df_Raw_Data = Df_Raw_Data.append(Df_Raw_File_Data)

	del Df_Raw_File_Data

	Df_Raw_Data["Email_Filtered"] = ""
	Mistakes = 0
	print("Start!")
	#If Headers_All is set to true, all headers are loaded. If False, only alternative is loaded.
	Headers_All = True
	if Headers_All:
	    List_Data_Headers = ["id", "date_sent", "date_received", "date_reported", "links", "sender_email", "recipient_email", "email_subject", "email_raw_headers", "email_raw_body", "email_has_attachments", "modified"] #List of all headers
	else:
	    List_Data_Headers = ["sender_email"]

	List_Data_Dates = ["date_sent", "date_received", "date_reported"] #List for all headers where the data has the format "timestamp". Datatype is np.int64

	for Header in List_Data_Headers: #Loop over all Columns
	    for Index in range(0, len(Df_Raw_Data)): #Loop over all Rows.
	        Data = Df_Raw_Data.loc[Index,Header] #Retreive value and assign it to "Data".
	        #print(str(Index) + " " + Header) #Prints current Column and Row for Debugging purposes.
	        
	        if Header in List_Data_Dates: #Checks if Data is in format Timestamp by comparing Headers.
	            if Data > 0: #Timestamp has to be positive. This is not the case in the raw data, this needs to be addressed.
	                Data = pd.datetime.fromtimestamp(Data) #Convert Timestamp to DateTime format using Pandas.
	                Df_Raw_Data.loc[Index, Header] = Data #Assigns DateTime format to Cell in Df_Raw_Data.
	        elif Header == "sender_email": #Checks if entry may contain email address.
	            Mail_Address = Fn.Retreive_Email_Addresses(Data)
	            if len(Mail_Address) == 1:
	                Df_Raw_Data.loc[Index, "Email_Filtered"] = Mail_Address[0]
	            elif len(Mail_Address) == 0:
	                Df_Raw_Data.loc[Index, "Email_Filtered"] = "Something went wrong. No Email Address was found."
	            elif Mail_Address[0] == Mail_Address[len(Mail_Address) - 1]:
	                Df_Raw_Data.loc[Index, "Email_Filtered"] = Mail_Address[0]
	                
	            
	            
	    
	        


	#Write to CSV
	if True:
	    Df_Raw_Data.to_csv("D:/Bachelor_Thesis/Email_Extraction/Raw_Data_Csv_File_" + Filename + ".csv")