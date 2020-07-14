# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:33:55 2020

@author: Kylian Rijnbergen
"""

import pandas as pd
import class_mailvector

Df_Data = pd.read_excel("vector_data.xlsx")[["Column1", "body_readable", "IsPhishing"]]

df_vectorized_emails = pd.DataFrame(columns = ["email_id", "word_matrix"])
for index in range(0, len(Df_Data)):
    identifier = Df_Data.loc[index, ["Column1"]]
    body = Df_Data.loc[index, ["body_readable"]]
    email = class_mailvector.MailVector(identifier, body)
    email.get_email_vector()
    df_vectorized_emails.loc[index, ["email_id"]] = identifier[0]
    df_vectorized_emails.loc[index, ["word_matrix"]] = email.word_vectors.values[0][0] #Currently only writes the first token in an email to the dataframe. Change to write the email vector for the email, and maybe also the email vector for the nouns.
    
    
    
    

    
    