# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 15:00:17 2020

@author: Kylian Rijnbergen
"""
import pandas as pd
data = pd.read_fwf('glove.840B.300d.txt', sep=" ", header=None, engine = "python")

words = []
for i in range(len(data)):
    string = data[0][i]
    split_string = string.split(" ")
    word = split_string[0]
    words.append(word)

df_words = pd.DataFrame(data = {"Words": words})
df_words.to_csv("glove.840B.300d_words.csv", sep = ",", index = False)