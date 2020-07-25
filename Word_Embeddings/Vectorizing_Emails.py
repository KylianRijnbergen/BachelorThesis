from timeit import default_timer as timer
import pandas as pd
import numpy as np
from class_mailvector import MailVector

start1 = timer()
VECTOR_DIMENSIONS = 300
VECTOR_DIMENSIONS_LIST = np.arange(0,VECTOR_DIMENSIONS).tolist()
COLUMN_HEADERS_LIST = [ 
        "ID",
        "Label"
        ]

column_list = COLUMN_HEADERS_LIST + VECTOR_DIMENSIONS_LIST

df_data = pd.read_excel("to_vectorize.xlsx")[["Column1", "body_readable", "IsPhishing"]]


df_vectorized_emails = pd.DataFrame(columns = column_list)

end1 = timer()
print("Time is " + str(end1 - start1))
for index in range(0, len(df_data)):
    start_timer2 = timer()
    print(index)
    df_vectorized_emails.loc[index, "ID"] = df_data.loc[index, "Column1"]
    df_vectorized_emails.loc[index, "Label"] = df_data.loc[index, "IsPhishing"]
    body = df_data.loc[index, "body_readable"]
    weighted_vector = MailVector(body).weighted_vector
    for i in range(1,301):
        dim = i - 1
        df_vectorized_emails.loc[index, dim] = weighted_vector[i-1]
    end_timer2 = timer()
    print("Time is " + str(end_timer2 - start_timer2))
        
df_vectorized_emails.to_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/" + str(VECTOR_DIMENSIONS) + "_Dimensions_Weighted_Test.csv")