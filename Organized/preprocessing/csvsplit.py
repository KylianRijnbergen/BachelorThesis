import pandas as pd
import math
import os

current_dir = os.getcwd().replace('\\', '/')

def train_test_split(
        filename = "nan_removed.csv", 
        test_size = 0.2, 
        random_state = 0, 
        part1_name = "part_1.csv",
        part2_name = "part_2.csv",
        subdir = "/data/Labelled_Emails_Features_Only/Word_Vectors/"
        ):

    df = pd.read_csv(current_dir + subdir + filename)
    df = df.sample(frac=1, random_state = random_state).reset_index(drop=True)
    row_count = len(df)
    split_at = math.floor(row_count * (1 - test_size))

    part_1 = df[0 : split_at]
    part_2 = df[split_at :]

    part_1.to_csv(current_dir + subdir + part1_name, index = False)
    part_2.to_csv(current_dir + subdir + part2_name, index = False)
    return