# Import 
import base64 #Used for encoding/decoding of base64 strings
from nltk.parse import CoreNLPParser
import html2text as h2t
import re as regex
from collections import Counter
import chardet
import random
import DataFrameFunctions as DfFun #Import DataFrameFunctions
import email


def ListToString(List, Delimiter = " "):
	if isinstance(List, list):
		return Delimiter.join(str(v) for v in List )
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

def HTML_To_Text(HTML):
	Plain_Text = h2t.html2text(HTML)
	#The current version of the html2text module is broken. using config.py
	return Plain_Text

#Fetch Email Address
def Retreive_Email_Addresses(Email_String):
    regex_Email_Address = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}' #regex to recognise email address
    Email = regex.findall(regex_Email_Address, str(Email_String))
    Email_No_Dupes = RemoveDuplicates(Email)
    return Email_No_Dupes

#Fetch links in text
def Retreive_URLs(String):
	regex_URL = '[A-Za-z0-9._%+-]+\.[A-Za-z0-9.-]+\.[A-Za-z/=()@.0-9_?&]{2,400}'
	URL = regex.findall(regex_URL, str(String))
	URL_No_Dupes = RemoveDuplicates(URL)
	return URL_No_Dupes

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

def DetectEncoding(String):
    if isinstance(String, str):
    	ByteArray = bytearray()
    	ByteArray.extend(map(ord, String))
    	Encoding = chardet.detect(ByteArray)
    	return Encoding
    
def Extract_HTML(String):
	StartIndex = String.lower().find("<html")
	print(StartIndex)
	EndIndex = String.lower().find("</html>")
	print(EndIndex)
	if StartIndex == EndIndex:
		return String
	else:
		return String[StartIndex: EndIndex + 7]

def Get_Relevant_Aspects(String):
	HTML_String = Extract_HTML(String)
	if HTML_String != String:
		HTML_String = HTML_To_Text(HTML_String)
		return HTML_String
	else:
		return String
	
def Print_Email(DataFrame_Row, DataFrame_Name):
	print("Email details: ")
	print("Sender: " + DataFrame_Name.loc[DataFrame_Row, "Sender_Email_Username"] + ": " + DataFrame_Name.loc[DataFrame_Row, "Sender_Email_Address"])
	print("Attachments: " + str(DataFrame_Name.loc[DataFrame_Row, "email_has_attachments"]))
	print("Subject: " + DataFrame_Name.loc[DataFrame_Row, "email_subject"])
	print("Raw body: ")
	TextList = DataFrame_Name.loc[DataFrame_Row, "readable_words"]
	TextString = ListToString(TextList)
	for line in TextString.splitlines():
		print(line)
	#print(DetectEncoding(TextString))


def Get_Data_Not_Seen(DataFrame_Name):
	UpperBound = DfFun.Get_DataFrame_RowCount(DataFrame_Name)
	RowToTake = random.randint(0, UpperBound - 1)
	if DataFrame_Name.loc[RowToTake, "Seen_Before"] == "1": 
		return Get_Data_Not_Seen(DataFrame_Name)
	else:
		return RowToTake

def GetEmailBody(MailString):
	MailMessage = email.message_from_string(MailString)
	Body = ""

	if MailMessage.is_multipart():
		for part in MailMessage.walk():
			ctype = part.get_content_type()

			if ctype == 'text/plain':
				Body = part.get_payload(decode=True)
	else: 
		Body = MailMessage.get_payload(decode=True)
	return Body

def ReturnMail(MailString): 
    MailMessage = email.message_from_string(MailString)
    body = "" 
    if MailMessage.is_multipart():
        print("Is Multipart")
    else: 
        print("is not Multipart")
	