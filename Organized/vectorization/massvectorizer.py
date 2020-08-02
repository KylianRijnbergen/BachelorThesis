from timeit import default_timer as timer
import pandas as pd
import numpy as np
from vectorizer import Vectorize


def get_shape(np_array):
    return np_array.shape[0]

start1 = timer()


df_data = pd.read_csv("D:/Bachelor_Thesis/GitHub/BachelorThesis/Organized/testfiles/preprocessed_mails.csv")[["body_readable", "IsPhishing"]]


np_vectorized_emails = np.empty([0,301])


for index in range(0, len(df_data)):
    start_timer2 = timer()
    print(index)
    body = df_data.loc[index, "body_readable"]
    label = df_data.loc[index, "IsPhishing"]
    weighted_vector = Vectorize(body).weighted_avg_vector
    weighted_vector_and_label = np.insert(weighted_vector, 0, label, axis = 0)
    
    insert_at = get_shape(np_vectorized_emails)
    np_vectorized_emails = np.insert(
            np_vectorized_emails, 
            insert_at,
            weighted_vector_and_label,
            axis = 0
            )

    end_timer2 = timer()
    print("Time is " + str(end_timer2 - start_timer2))
    
end1 = timer()
print("Time is " + str(end1 - start1))
        
pd.DataFrame(np_vectorized_emails).to_csv("D:/Bachelor_Thesis/GitHub/BachelorThesis/Organized/testfiles/vectorized_mails.csv")