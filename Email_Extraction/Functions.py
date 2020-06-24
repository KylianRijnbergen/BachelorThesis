# Import 
import base64 #Used for encoding/decoding of base64 strings
import numpy as np #Numpy library for arrays, tables and datastructures.
from nltk.parse import CoreNLPParser
import html2text as h2t
import re as regex
from collections import Counter
import pandas as pd


def ListToString(List, Delimiter = " "):
	if isinstance(List, list):
		return Delimiter.join(List)
	else:
		return List
    
def StringToList(List, Delimiter = " "):
	if isinstance(List, str):
		return List.split(Delimiter)
	else: 
		return List
    
# Decoding functions
#Base 64 ("=?utf-8?b?" && "?=")
def decodeBase64(encodedStr):
	if(encodedStr[:10].lower() == '=?utf-8?b?' and encodedStr[-2:] == '?='): #only base64 encoded strings
		encodedStr	= encodedStr[10:-2] #Removes first 10 and last 2 characters
		decodedBytes = base64.b64decode(encodedStr) #Decoding to base 64
		decodedStr = str(decodedBytes, "utf-8") #UTF-8 string
		return decodedStr #returns decoded string
	else:
		return encodedStr #returns encoded string

#The NER Tagger (part of CoreNLP) can be started by running Start_Server.bat in 'D:\Bachelor_Thesis\Email_Extraction\CoreNLP\stanford-corenlp-4.0.0'
def NER(word):
	ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
	Linguistic_Element_Type = ner_tagger.tag(word.split())
	return Linguistic_Element_Type

def HTML_To_Text(HTML_String):
    Plain_Text = h2t.html2text(HTML_String)
    return Plain_Text

#Fetch Email Address
def Retreive_Email_Addresses(Email_String):
    regex_Email_Address = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}' #regex to recognise email address
    Email = regex.findall(regex_Email_Address, str(Email_String))
    Email_No_Dupes = RemoveDuplicates(Email)
    return Email_No_Dupes

#Remove Email Address, return username (everything that is left)
def Get_Email_Username(Email_String, Email_Address):
	List_Sender_Email = StringToList(Email_String)
	#Remove duplicates using function below
	if List_Sender_Email[-1] == Email_Address: #check if last element is email address
		del List_Sender_Email[-1]
	return List_Sender_Email

def RemoveDuplicates(List_Unfiltered):
    DuplicatesRemoved = list(Counter(List_Unfiltered))
    return DuplicatesRemoved
    
def CutDataFrame(DataFrame_Name, Startrow, Endrow):
	Sliced_DataFrame = DataFrame_Name[Startrow: Endrow]
	return Sliced_DataFrame
