from timeit import default_timer as timer
import pandas as pd
import numpy as np
from class_mailvector_numpy_memo import MailVector

start1 = timer()


df_data = pd.read_csv("120925072020.csv")[["body_readable", "IsPhishing"]]


np_vectorized_emails = np.empty([0,301])


for index in range(0, len(df_data)):
    start_timer2 = timer()
    print(index)
    body = df_data.loc[index, "body_readable"]
    label = df_data.loc[index, "IsPhishing"]
    weighted_vector = MailVector(body).weighted_avg_vector
    weighted_vector_and_label = np.insert(weighted_vector, 0, label, axis = 0)
    
    np_vectorized_emails = np.insert(
            np_vectorized_emails, 
            np_vectorized_emails.shape[0],
            weighted_vector_and_label,
            axis = 0
            )

    end_timer2 = timer()
    print("Time is " + str(end_timer2 - start_timer2))
    
end1 = timer()
print("Time is " + str(end1 - start1))
        
pd.DataFrame(np_vectorized_emails).to_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/300_Dimensions_Weighted_np_vectorizer_Test.csv")