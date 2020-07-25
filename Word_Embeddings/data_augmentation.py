#File works, but is exponentially slow.

import pandas as pd
import random
import numpy as np

#Adjust randomization percentage.
RANDOMIZATION_FACTOR = 1.01 #This is a percentage-based randomizer.
#load data to dataframe
df_mail_vectors = pd.read_excel("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/300_Dimensions.xlsx", index_col = None)
#amount of rows
row_count = len(df_mail_vectors)

#Generate list of dimensions
indices = np.arange(0,300).tolist()
#Headers
COLUMNS = ["ID", "Label"] + indices

#df for storing augmented data
newly_created_data = pd.DataFrame(columns = COLUMNS)

#pull random row number 
for row_to_augment in range(0,row_count):
    print("Progress: " + str(row_to_augment) + "/" + str(row_count) + ".")
    #Empty DataFrame with correct headers
    new_row = pd.DataFrame(columns = COLUMNS)
    
    #Copy DataFrame entry to new df
    for v in COLUMNS:
        new_row.loc[0, v] = df_mail_vectors.loc[row_to_augment, v]
            
    #For each row.
    for dim in range (0, 300):        
        #Generate new number
        old_value = new_row.loc[0, dim]
        random_float = random.uniform(1/RANDOMIZATION_FACTOR, RANDOMIZATION_FACTOR)
        new_value = old_value * random_float
    
        #assign to df
        new_row.loc[0, dim] = new_value
        newly_created_data = newly_created_data.append(new_row)
        
newly_created_data.to_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/300_Dimensions_Weighted_Augmented.csv")