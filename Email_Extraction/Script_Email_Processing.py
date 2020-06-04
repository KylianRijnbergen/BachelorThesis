# Import 
import base64 #Used for encoding/decoding of base64 strings
import numpy as np #Numpy library for arrays, tables and datastructures.

def decodeBase64(encodedStr):
	if(encodedStr[:10] == '=?UTF-8?B?' and encodedStr[-2:] == '?='): #only base64 encoded strings
		encodedStr	= encodedStr[10:-2] #Removes first 10 and last 2 characters
		decodedBytes = base64.b64decode(encodedStr) #Decoding to base 64
		decodedStr = str(decodedBytes, "utf-8") #UTF-8 string
		return decodedStr #returns decoded string
	else:
		return encodedStr #returns encoded string

def split(string_to_split_array):
	splittedArray = np.empty(0, dtype=str)
	splits = string_to_split_array.split()
	for split in splits:
		splittedArray = np.append(splittedArray, split)
	return splittedArray

	