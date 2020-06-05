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

Array_Master = np.append(Array_IDS, Array_Raw_Date_Sent, axis = 1) #Adds Array_Raw_Date_Sent to the right of the Master Array

print(Array_Master) #Printing Results