import pandas as pd
import os
current_dir = os.getcwd().replace('\\', '/')
def load_data(
        current_dir = current_dir, 
        training_data = "part_1.csv", 
        testing_data = "part_2.csv"
        ): 
    Directory_Labelled_Emails = current_dir

    df_train = pd.read_csv(
            Directory_Labelled_Emails 
            + training_data
            )

    df_test = pd.read_csv(
            Directory_Labelled_Emails 
            + testing_data
            )

    X_train = df_train.iloc[:, 1:302]
    y_train = df_train.iloc[:, 0]
    X_test = df_test.iloc[:, 1:302]
    y_test = df_test.iloc[:, 0]

    return X_train, y_train, X_test, y_test