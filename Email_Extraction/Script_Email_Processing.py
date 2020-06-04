# Import libraries
import numpy as np

def decodeBase64(encodedStr):
	if(encodedStr[:10] == '=?UTF-8?B?' and encodedStr[-2:] == '?='): #only base64 encoded strings