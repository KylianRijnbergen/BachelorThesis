# Import 
import base64 #Used for encoding/decoding of base64 strings


def decodeBase64(encodedStr):
	if(encodedStr[:10] == '=?UTF-8?B?' and encodedStr[-2:] == '?='): #only base64 encoded strings
		encodedStr	= encodedStr[10:-2] #Removes first 10 and last 2 characters
		decodedBytes = base64.b64decode(encodedStr) #Decoding to base 64
		decodedStr = str(decodedBytes, "utf-8") #UTF-8 string
		return decodedStr #returns decoded string
	else:
		return encodedStr #returns encoded string

