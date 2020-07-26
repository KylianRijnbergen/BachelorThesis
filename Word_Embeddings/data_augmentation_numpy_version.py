import numpy as np
import pandas as pd

#Adjust randomization percentage.
RANDOMIZATION_FACTOR = 1.02 #This is a percentage-based randomizer.
AUGMENTATION_FREQUENCY = 10


df_mail_vectors = pd.read_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/part_1.csv", index_col = None)
np_augmented_data = df_mail_vectors.to_numpy(copy = True)
#np_augmented_data = np.delete(np_augmented_data, 0, 1)
np_mail_vectors = df_mail_vectors.to_numpy(copy = True)
del df_mail_vectors
#np_mail_vectors = np.delete(np_mail_vectors, 0, 1)
row_count = len(np_mail_vectors)

np_ones = np.ones(row_count)

for i in range(0, AUGMENTATION_FREQUENCY):
    random_numbers_matrix = np.random.normal(1, RANDOMIZATION_FACTOR - 1, (row_count, 300))
    np_multiplication_matrix = np.insert(random_numbers_matrix, 0, np_ones, axis = 1)
    del random_numbers_matrix

    output = np.multiply(np_mail_vectors, np_multiplication_matrix)

    np_augmented_data = np.insert(np_augmented_data, 0, output, axis = 0)


pd.DataFrame(np_augmented_data).to_csv("D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/part_1_augmented.csv", index = False)