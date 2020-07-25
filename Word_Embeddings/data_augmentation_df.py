import pandas as pd
import numpy as np

#Adjust randomization percentage.
RANDOMIZATION_FACTOR = 1.03 #This is a percentage-based randomizer.
AUGMENTATION_FREQUENCY = 10 #Set amount of times the data should be duplicated.
#load data to dataframe
df_mail_vectors = pd.read_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/part_1.csv", index_col = None)
#amount of rows
row_count = len(df_mail_vectors)

#Generate list of dimensions
indices = np.arange(0,300).tolist()
#Headers
COLUMNS = ["ID", "Label"] + indices

#df for storing augmented data
newly_created_data = pd.DataFrame(columns = COLUMNS)

for index in range(0, AUGMENTATION_FREQUENCY):
    #pull random row number 
    for row_to_augment in range(0, row_count):
        print("Progress: " + str(row_to_augment + index * row_count) + "/" + str(row_count * AUGMENTATION_FREQUENCY) + ".")
        #Empty DataFrame with correct headers
        new_row = pd.DataFrame(columns = COLUMNS)
        
        #Copy DataFrame entry to new df
        for v in COLUMNS:
            new_row.loc[0, v] = df_mail_vectors.loc[row_to_augment, str(v)]
            
        newly_created_data.loc[row_to_augment + index * row_count, "ID"] = "Fake"
        newly_created_data.loc[row_to_augment + index * row_count, "Label"] = new_row.loc[0, "Label"]        
        #For each row.
        for dim in range(0, 300):     
            #Generate new number
            old_value = new_row.loc[0, dim]
            random_float = np.random.normal(1, RANDOMIZATION_FACTOR -1)
            new_value = old_value * random_float
        
            if True: #probability of modifying a dimension.
                newly_created_data.loc[row_to_augment + index * row_count, dim] = new_value
            else:
                newly_created_data.loc[row_to_augment + index * row_count, dim] = old_value
        
newly_created_data.to_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/part_1.csv", index = False)