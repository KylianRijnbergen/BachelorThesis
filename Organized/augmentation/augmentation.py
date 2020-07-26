import numpy as np
import pandas as pd

def augment(
        file_directory,
        filename,
        randomization_factor,
        augmentation_frequency,
        writing_directory
        ):
    
    df = pd.read_csv(
            file_directory + filename,
            index_col = None
            )

    np_data = df.to_numpy(copy = True)
    np_augmented = np.copy(np_data)
    np_ones = np.ones(len(np_data))

    for _ in range(0, augmentation_frequency):
        np_random = np.random.normal(
                1, 
                randomization_factor - 1, 
                (len(np_data), 300)
                )
        np_random = np.insert(
                np_random,
                0, 
                np_ones, 
                axis = 1
                )
        
        output = np.multiply(np_data, np_random)
        np_augmented = np.insert(np_augmented, 0, output, axis = 0)
    
    pd.DataFrame(np_augmented).to_csv(
            writing_directory 
            + filename,
            index = False
            )