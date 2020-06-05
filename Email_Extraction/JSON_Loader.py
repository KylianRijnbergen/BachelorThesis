import json #Imports JSON Handler
import numpy as np #Importing Numpy


with open('C:/Users/Kylian Rijnbergen/Documents/TBK/Year_3/Module 12/Email_Extraction/phishing_mails_2018-06-02_nl.json') as file: #Opens JSON File
    data = json.load(file)  #Loads Values to "data"  


Array_IDS_Values = np.array(list(data['id'].items()))   #Fetches "id"
Array_IDS_Header = ["Index", "ID"]  #Header for IDS array
Array_IDS = np.vstack([Array_IDS_Header, Array_IDS_Values]) #Adding header to top of Values

Array_Date_Sent_Values = np.array(list(data['date_sent'].items()))  #Fetches "date_sent"
Array_Date_Sent_Header = ["Index", "DateSent"]  #Header for Date_Sent array
Array_Date_Sent = np.vstack([Array_Date_Sent_Header, Array_Date_Sent_Values]) #Adding header on top of Values
Array_Raw_Date_Sent = np.delete(Array_Date_Sent, 0, axis = 1) #Deletes "Index" Column

Array_Date_Received_Values = np.array(list(data['date_received'].items()))  #Fetches "date_received"
Array_Date_Received_Header = ["Index", "DateReceived"]  #Header for Date_Received array
Array_Date_Received = np.vstack([Array_Date_Received_Header, Array_Date_Received_Values]) #Adding header on top of Values
Array_Raw_Date_Received = np.delete(Array_Date_Received, 0, axis = 1) #Deletes "Index" Column

#Array_Links_Values = np.array(list(data['links'].items()))  #Fetches "links"
#Array_Links_Header = ["Index", "Links"]  #Header for links array
#Array_Links = np.vstack([Array_Links_Header, Array_Links_Values]) #Adding header on top of Values
#Array_Raw_Links = np.delete(Array_Links, 0, axis = 1) #Deletes "Index" Column

Array_Sender_Email_Values = np.array(list(data['sender_email'].items()))  #Fetches "Sender_Email"
Array_Sender_Email_Header = ["Index", "SenderEmail"]  #Header for Sender_Email array
Array_Sender_Email = np.vstack([Array_Sender_Email_Header, Array_Sender_Email_Values]) #Adding header on top of Values
Array_Raw_Sender_Email = np.delete(Array_Sender_Email, 0, axis = 1) #Deletes "Index" Column



Array_Master = np.concatenate((Array_IDS, Array_Raw_Date_Sent, Array_Raw_Date_Received, Array_Raw_Sender_Email), axis = 1) #Adds Array_Raw_Date_Sent, Array_Date_Received to the right of the Master Array

print(Array_Master) #Printing Results